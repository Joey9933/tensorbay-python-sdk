#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file handles with the ImageEmotion dataset"""

import csv
import os

from ...dataset import Data, Dataset
from ...label import Classification
from .._utility import glob

DATASET_NAME_ABSTRACT = "ImageEmotionAbstract"
DATASET_NAME_ARTPHOTO = "ImageEmotionArtphoto"


def ImageEmotionAbstract(path: str) -> Dataset:
    """ImageEmotionAbstract open dataset dataloader

    :param path: Path to ImageEmotionAbstract dataset
    The file structure should be like:
    <path>
        ABSTRACT_groundTruth.csv
        abstract_xxxx.jpg
        ...

    :return: load `Dataset` object
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME_ABSTRACT)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog_abstract.json"))
    segment = dataset.create_segment()

    csv_path = os.path.join(root_path, "ABSTRACT_groundTruth.csv")
    with open(csv_path, "r") as fp:
        reader = csv.DictReader(fp)
        reader.fieldnames = [
            field.strip("'") for field in reader.fieldnames  # type:ignore[union-attr]
        ]

        for row in reader:
            image_path = os.path.join(root_path, row.pop("").strip("'"))

            data = Data(image_path)
            values = {key: int(value) for key, value in row.items()}

            data.labels.classification = Classification(attributes=values)
            segment.append(data)

    return dataset


def ImageEmotionArtphoto(path: str) -> Dataset:
    """ImageEmotionArtphoto open dataset dataloader

    :param path: Path to ImageEmotionArtphoto dataset
    The file structure should be like:
    <path>
        <filename>.jpg
        ...

    :return: load `Dataset` object
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME_ARTPHOTO)
    dataset.load_catalog(os.path.join(os.path.dirname(__file__), "catalog_artphoto.json"))
    segment = dataset.create_segment()

    image_paths = glob(os.path.join(root_path, "*.jpg"))

    for image_path in image_paths:
        image_category = os.path.basename(image_path).split("_", 1)[0]

        data = Data(image_path)
        data.labels.classification = Classification(category=image_category)
        segment.append(data)

    return dataset