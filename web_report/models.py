"""The database works logic."""

from peewee import IntegerField, Model, SqliteDatabase, TextField
from playhouse.shortcuts import model_to_dict


class Racers(Model):
    """The database model implementing class.

    Args:
        Model (class): The class Racers inherit
    """
    position = IntegerField(null=False)
    abr = TextField(primary_key=True)
    racer_name = TextField(null=False)
    team = TextField(null=False)
    time = TextField(null=False)


def db_to_dict_for_json_xml(database_path: str) -> dict:
    """Convert database data to dict, with the abreviations as keys...
    ... and the driver statistic elements dicts as values.

    Args:
        database_path (str): Database file path

    Returns:
        dict: a xml-or-json format usable dict
    """
    Racers.bind(SqliteDatabase(database_path))
    racers = Racers.select()
    result = {}
    for item in racers.execute():
        record = model_to_dict(item)
        result[record.pop('abr')] = record
    return result


def db_to_list_for_html(database_path: str, sep: str) -> list:
    """Convert db data to list of strings of stocke values.

    Args:
        database_path (str): Database file path
        sep (str): seporator between a values at the line

    Returns:
        list: a html chart making usable one
    """
    Racers.bind(SqliteDatabase(database_path))
    racers = Racers.select()
    result = []
    for item in racers.execute():
        record = model_to_dict(item, exclude=[Racers.abr])
        record['position'] = str(record['position'])
        result.append(sep.join(list(record.values())))
    return result


def get_drivers_and_codes(database_path: str) -> dict:
    """Convert db data to a dict with abreviations as keys...
    ... and racers names as values.

    Args:
        database_path (str): Database file path

    Returns:
        dict: name-codelink chart making usable one
    """
    Racers.bind(SqliteDatabase(database_path))
    racers = Racers.select(Racers.racer_name, Racers.abr)
    result = {}
    for item in racers.execute():
        record = model_to_dict(item, only=[Racers.racer_name, Racers.abr])
        result[record['abr']] = record['racer_name']
    return result


def get_driver_statistic(database_path: str, code: str) -> dict:
    """Get db record to name and statistic string dict

    Args:
        database_path (str): Database file path
        code (str): abbreviation

    Returns:
        dict: user statistic making usable one
    """
    Racers.bind(SqliteDatabase(database_path))
    driver = Racers.get_by_id(code)
    name = driver.racer_name
    record = model_to_dict(driver, exclude=[Racers.abr, Racers.racer_name])
    record['position'] = str(record['position'])
    return {
        'name': name,
        'driver_statistic': ' |'.join(list(record.values())),
        }
