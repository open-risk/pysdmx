import pytest
import tests.fmr.vl_code_checks as checks

from pysdmx.api.fmr import AsyncRegistryClient, Format, RegistryClient


@pytest.fixture()
def fmr():
    return RegistryClient(
        "https://registry.sdmx.org/sdmx/v2/",
        Format.FUSION_JSON,
    )


@pytest.fixture()
def async_fmr():
    return AsyncRegistryClient(
        "https://registry.sdmx.org/sdmx/v2/",
        Format.FUSION_JSON,
    )


@pytest.fixture()
def q1(fmr):
    res = "structure/codelist/"
    agency = "TEST"
    id = "CTYPES"
    version = "1.0"
    return f"{fmr.api_endpoint}{res}{agency}/{id}/{version}"


@pytest.fixture()
def q2(fmr):
    res = "structure/valuelist/"
    agency = "TEST"
    id = "CTYPES"
    version = "1.0"
    return f"{fmr.api_endpoint}{res}{agency}/{id}/{version}"


@pytest.fixture()
def body():
    with open("tests/fmr/samples/code/vl.fusion.json", "rb") as f:
        return f.read()


def test_returns_codelist_from_vl(respx_mock, fmr, q1, q2, body):
    """get_codelist() should return a codelist with the expected codes."""
    checks.check_vl_codelist(respx_mock, fmr, q1, q2, body)


@pytest.mark.asyncio()
async def test_codes_from_vl_have_core_info(
    respx_mock,
    async_fmr,
    q1,
    q2,
    body,
):
    """Codes must contain core information such as ID and name."""
    await checks.check_vl_code_expected_info(
        respx_mock,
        async_fmr,
        q1,
        q2,
        body,
    )
