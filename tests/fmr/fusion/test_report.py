import pytest
import tests.fmr.report_checks as checks

from pysdmx.fmr import AsyncRegistryClient, Format, RegistryClient


@pytest.fixture()
def fmr():
    return RegistryClient(
        "https://registry.sdmx.org/sdmx/v2/",
        Format.FUSION_JSON,
    )


@pytest.fixture()
def async_fmr() -> AsyncRegistryClient:
    return AsyncRegistryClient(
        "https://registry.sdmx.org/sdmx/v2/",
        Format.FUSION_JSON,
    )


@pytest.fixture()
def query(fmr):
    res = "metadata/metadataset/"
    provider = "BIS.MEDIT"
    id = "DTI_BIS_MACRO"
    version = "1.0"
    return f"{fmr.api_endpoint}{res}{provider}/{id}/{version}"


@pytest.fixture()
def body():
    with open("tests/fmr/samples/refmeta/report.fusion.json", "rb") as f:
        return f.read()


def test_returns_report(respx_mock, fmr, query, body):
    """get_hierarchy() should return a metadata report."""
    checks.check_report(respx_mock, fmr, query, body)


@pytest.mark.asyncio()
async def test_attributes(respx_mock, async_fmr, query, body):
    """Report contains the expected attributes."""
    await checks.check_attributes(respx_mock, async_fmr, query, body)
