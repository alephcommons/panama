import os
import sys
import tarfile
import logging
from lxml import html
from pprint import pprint  # noqa
from banal import ensure_list
from datetime import datetime
from normality import collapse_spaces
from followthemoney import model
from followthemoney.cli.util import write_object
from ftmstore import Dataset

NO_AGENT = (
    "NO CONSTA",
    ".",
    "-NO TIENE-",
    "",
    "1",
    ". 1",
    "_____NO CONSTA::::",
    "NO",
    None,
)

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
log = logging.getLogger("panama")


def text(el):
    for el in ensure_list(el):
        return el.text_content().strip()


def clean_text(text):
    text = collapse_spaces(text)
    if text is None:
        return
    text = text.strip("-")
    return collapse_spaces(text)


def date(el):
    # print("ELLLL", text(el))
    value = text(el)
    if value is None:
        return
    for fmt in ("%d-%m-%Y", "00-00-%Y"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.date().isoformat()
        except ValueError:
            pass
    # if value is not None and len(value.strip()):
    #     print("FAILED_DATE", value)


def is_valid(name):
    if name is None:
        return False
    name = name.rstrip("1").strip("-").strip()
    if name in NO_AGENT:
        return False
    if "NO CONSTA" in name:
        return False
    return True


def parse_filing(doc):
    content = doc.xpath("//body/table/tr[4]/td[2]")[0]
    company = model.make_entity("Company")
    file_number = text(content.xpath("./table[1]/tr/td[2]"))
    # doc_number = text(content.xpath("./table[1]/tr/td[4]"))
    company_name = text(content.xpath("./table[3]/tr[1]/td"))
    company.make_id(company_name, file_number)
    company.add("jurisdiction", "pa")
    company.add("name", company_name)
    company.add("registrationNumber", file_number)
    reg_date = date(content.xpath("./table[5]/tr/td[2]"))
    company.add("incorporationDate", reg_date)
    dis_date = date(content.xpath("./table[34]/tr/td[2]"))
    company.add("dissolutionDate", dis_date)
    status = text(content.xpath("./table[5]/tr/td[4]"))
    company.add("status", status)
    writing_date = date(content.xpath("./table[6]/tr/td[4]"))
    company.add("modifiedAt", writing_date)
    location = text(content.xpath("./table[9]/tr/td[4]"))
    company.add("address", location)

    currency = text(content.xpath("./table[18]/tr/td[2]"))
    company.add("currency", currency)
    capital = text(content.xpath("./table[19]/tr/td[2]"))
    company.add("capital", capital)
    capital_notes = text(content.xpath("./table[21]"))
    capital_notes = clean_text(capital_notes)
    if is_valid(capital_notes):
        company.add("notes", capital_notes)
    repres_notes = text(content.xpath("./table[23]"))
    repres_notes = clean_text(repres_notes)
    if is_valid(repres_notes):
        company.add("notes", repres_notes)

    description = text(content.xpath("./table[42]"))
    description = clean_text(description)
    if is_valid(description):
        company.add("description", clean_text(description))

    agent_name = text(content.xpath("./table[13]/tr/td[2]"))
    agent_name = clean_text(agent_name)
    if is_valid(agent_name):
        agent = model.make_entity("LegalEntity")
        agent.make_id("agent", agent_name)
        agent.add("name", agent_name)
        agent.add("country", "pa")
        yield agent

        repres = model.make_entity("Representation")
        repres.make_id("Respresentation", company.id, agent.id)
        repres.add("client", company)
        repres.add("agent", agent)
        repres.add("role", "Agente Residente")
        yield repres

    dignitaries = set()
    for dignitary in content.xpath("./table[25]/tr"):
        role, name = dignitary.findall("./td")
        role, name = text(role), text(name)
        if not is_valid(name):
            continue
        dignitaries.add(name)

        person = model.make_entity("Person")
        person.make_id(company.id, name)
        person.add("name", name)
        yield person

        link = model.make_entity("Directorship")
        link.make_id("Directorship", company.id, person.id)
        link.add("organization", company)
        link.add("director", person)
        link.add("role", role)
        yield link

    for director in content.xpath("./table[27]/tr"):
        name = text(director)
        if name in dignitaries:
            continue
        if not is_valid(name):
            continue

        person = model.make_entity("Person")
        person.make_id(company.id, name)
        person.add("name", name)
        yield person

        link = model.make_entity("Directorship")
        link.make_id("Directorship", company.id, person.id)
        link.add("organization", company)
        link.add("director", person)
        link.add("role", "Director")
        yield link

    for subscriber in content.xpath("./table[29]/tr"):
        name = text(subscriber)
        if not is_valid(name):
            continue
        entity = model.make_entity("LegalEntity")
        entity.make_id(company.id, name)
        entity.add("name", name)
        yield entity

        link = model.make_entity("Ownership")
        link.make_id("Ownership", company.id, entity.id)
        link.add("asset", company)
        link.add("owner", entity)
        link.add("role", "Suscriptor")
        yield link

    # pprint(company.to_dict())
    yield company


def parse_file(writer, fh, member):
    try:
        doc = html.parse(fh)
        for idx, entity in enumerate(parse_filing(doc)):
            if entity.id is None:
                raise ValueError("Invalid document, no company ID.")
            fragment = "%s.%d" % (member.name, idx)
            writer.put(entity, fragment=fragment)
    except Exception:
        log.exception("Failed to parse: %r", member)


def parse_archive(writer, archive_path):
    log.info("Archive: %s", archive_path)
    tar = tarfile.open(archive_path, "r")
    while True:
        member = tar.next()
        if member is None:
            break
        fh = tar.extractfile(member)
        if fh is None:
            continue
        parse_file(writer, fh, member)
        fh.close()
    writer.flush()


if __name__ == "__main__":
    prefix = "data/"
    dataset = Dataset("pa_companies", origin="parse")
    writer = dataset.bulk()
    for file_name in sorted(os.listdir(prefix)):
        file_path = os.path.join(prefix, file_name)
        parse_archive(writer, file_path)

    with open("panama.json", "w") as fh:
        for entity in dataset.iterate():
            write_object(fh, entity)
