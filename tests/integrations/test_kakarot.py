import pytest
from starkware.starknet.testing.contract import StarknetContract

from tests.integrations.test_cases import params_execute
from tests.utils.utils import (
    extract_memory_from_execute,
    extract_stack_from_execute,
    hex_string_to_bytes_array,
    traceit,
)


@pytest.mark.asyncio
class TestKakarot:
    @pytest.mark.parametrize(
        "params",
        params_execute,
    )
    async def test_execute(self, kakarot: StarknetContract, params: dict, request):
        with traceit.context(request.node.callspec.id):
            res = await kakarot.execute(
                value=int(params["value"]),
                bytecode=hex_string_to_bytes_array(params["code"]),
                calldata=hex_string_to_bytes_array(params["calldata"]),
            ).call(caller_address=1)

        stack_result = extract_stack_from_execute(res.result)
        memory_result = extract_memory_from_execute(res.result)

        assert stack_result == (
            [int(x) for x in params["stack"].split(",")] if params["stack"] else []
        )
        assert memory_result == hex_string_to_bytes_array(params["memory"])

        events = params.get("events")
        if events:
            assert [
                [
                    event.keys,
                    event.data,
                ]
                for event in sorted(res.call_info.events, key=lambda x: x.order)
            ] == events
