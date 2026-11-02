"""
Common utility functions for weather data processing tasks.
"""
import csv
import json
import logging
import os
import sys
from typing import Any, Dict, Iterable, Mapping, TextIO, Type, Union

from pydantic import BaseModel

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def get_logger(source_file: str) -> logging.Logger:
    """
    Get a logger named after the task file (e.g. "task1_scrape"), even when run as a script.

    Args:
        source_file (str): The calling module's `__file__`.

    Returns:
        logging.Logger: The module logger.
    """
    return logging.getLogger(os.path.splitext(os.path.basename(source_file))[0])


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure console logging for the task scripts.

    Args:
        level (int): Minimum log level to output.
    """
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    logging.basicConfig(level=level, format=LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")


logger = get_logger(__file__)


def data_path(filename: str) -> str:
    """
    Build the absolute path of a sample data file stored next to the task scripts.

    Args:
        filename (str): Name of the file inside the `src` directory.

    Returns:
        str: Absolute path to the file.
    """
    return os.path.join(DATA_DIR, filename)


def load_json(filename: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict: The loaded JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filename}' was not found.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding JSON from '{filename}': {e.msg}", e.doc, e.pos)


def save_to_json(data: Union[Dict[str, Any], BaseModel], filename: str) -> None:
    """
    Save data to a JSON file.

    Args:
        data (dict or BaseModel): The data to be saved to the JSON file.
        filename (str): The name of the JSON file to save the data in.

    Raises:
        IOError: If there is an error writing to the file.
    """
    if isinstance(data, BaseModel):
        data = data.model_dump()
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info("Saved JSON to %s", filename)
    except IOError as e:
        raise IOError(f"Error writing to file '{filename}': {e}")


def csv_headers(model: Type[BaseModel]) -> list:
    """
    Get CSV column headers for a model: each field's serialization alias (or its name).

    Args:
        model (type[BaseModel]): The row model.

    Returns:
        list of str: Column headers in field order.
    """
    return [field.serialization_alias or name for name, field in model.model_fields.items()]


def save_models_to_csv(records: Iterable[Union[Mapping[str, Any], BaseModel]],
                       model: Type[BaseModel],
                       file: Union[str, TextIO]) -> None:
    """
    Validate records with a Pydantic model and write them to a CSV file or file-like object.

    Column headers come from the model's field aliases (see `csv_headers`).

    Args:
        records (iterable of dict or BaseModel): Rows to write.
        model (type[BaseModel]): Model describing one CSV row.
        file (str or file-like object): Destination path or an open text stream.

    Raises:
        IOError: If there is an error writing to the file.
        pydantic.ValidationError: If a record does not match the model.
    """
    rows = [
        model.model_validate(r.model_dump() if isinstance(r, BaseModel) else r).model_dump(by_alias=True)
        for r in records
    ]

    def write(stream: TextIO) -> None:
        writer = csv.DictWriter(stream, fieldnames=csv_headers(model))
        writer.writeheader()
        writer.writerows(rows)

    if not isinstance(file, str):
        write(file)
        logger.debug("Wrote %d %s rows to a stream", len(rows), model.__name__)
        return
    try:
        with open(file, 'w', newline='', encoding='utf-8') as f:
            write(f)
        logger.info("Saved %d rows to %s", len(rows), file)
    except IOError as e:
        raise IOError(f"Error writing to file '{file}': {e}")
