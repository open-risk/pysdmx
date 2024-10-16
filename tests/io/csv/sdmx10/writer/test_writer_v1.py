from io import StringIO
from pathlib import Path

import pandas as pd
import pytest

from pysdmx.io.csv.sdmx10.writer import writer
from pysdmx.model.dataset import PandasDataset


@pytest.fixture()
def data_path():
    base_path = Path(__file__).parent / "samples" / "df.json"
    return str(base_path)


@pytest.fixture()
def data_path_reference():
    base_path = Path(__file__).parent / "samples" / "reference.csv"
    return str(base_path)


@pytest.fixture()
def data_path_reference_atch_atts():
    base_path = Path(__file__).parent / "samples" / "reference_attch_atts.csv"
    return str(base_path)


def test_to_sdmx_csv_writing(data_path, data_path_reference):
    urn = "urn:sdmx:org.sdmx.infomodel.datastructure.DataFlow=MD:DS1(1.0)"
    dataset = PandasDataset(
        attributes={},
        data=pd.read_json(data_path, orient="records"),
        structure=urn,
    )
    dataset.data = dataset.data.astype("str")
    result_sdmx_csv = writer(dataset)
    result_df = pd.read_csv(StringIO(result_sdmx_csv)).astype(str)
    reference_df = pd.read_csv(data_path_reference).astype(str)
    pd.testing.assert_frame_equal(
        result_df.fillna("").replace("nan", ""),
        reference_df.replace("nan", ""),
        check_like=True,
    )


def test_writer_attached_attrs(data_path, data_path_reference_atch_atts):
    urn = "urn:sdmx:org.sdmx.infomodel.datastructure.DataFlow=MD:DS1(1.0)"
    dataset = PandasDataset(
        attributes={"DECIMALS": 3},
        data=pd.read_json(data_path, orient="records"),
        structure=urn,
    )
    dataset.data = dataset.data.astype("str")
    result_sdmx_csv = writer(dataset)
    result_df = pd.read_csv(StringIO(result_sdmx_csv)).astype(str)
    reference_df = pd.read_csv(data_path_reference_atch_atts).astype(str)
    pd.testing.assert_frame_equal(
        result_df.fillna("").replace("nan", ""),
        reference_df.replace("nan", ""),
        check_like=True,
    )
