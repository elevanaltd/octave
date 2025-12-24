"""Tests for octave_amend MCP tool (Epic #41, Issue #41 Phase 2).

Tests the amend tool capabilities:
- Amend existing OCTAVE files with updates
- Track corrections (W001-W005)
- Return compact diff by default
- Optional base_hash consistency check
- Merge changes into existing content
"""

import os
import tempfile

import pytest

from octave_mcp.mcp.amend import AmendTool
from octave_mcp.mcp.create import CreateTool


class TestAmendTool:
    """Test AmendTool MCP tool."""

    def test_tool_metadata(self):
        """Test tool has correct metadata."""
        tool = AmendTool()

        assert tool.get_name() == "octave_amend"
        assert "amend" in tool.get_description().lower()
        assert "octave" in tool.get_description().lower()

    def test_tool_schema(self):
        """Test tool input schema."""
        tool = AmendTool()
        schema = tool.get_input_schema()

        # Required parameters
        assert "target_path" in schema["properties"]
        assert "changes" in schema["properties"]
        assert "target_path" in schema["required"]
        assert "changes" in schema["required"]

        # Optional parameters
        assert "base_hash" in schema["properties"]

    @pytest.mark.asyncio
    async def test_amend_simple_field(self):
        """Test amending a simple field value."""
        create_tool = CreateTool()
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "test.oct.md")

            # Create initial file
            create_result = await create_tool.execute(
                content="===TEST===\nKEY::value1\n===END===",
                target_path=target_path,
            )
            assert create_result["status"] == "success"
            original_hash = create_result["canonical_hash"]

            # Amend the file
            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"KEY": "value2"},
            )

            # Verify result structure
            assert amend_result["status"] == "success"
            assert amend_result["path"] == target_path
            assert "canonical_hash" in amend_result
            assert amend_result["canonical_hash"] != original_hash  # Hash changed
            assert "corrections" in amend_result
            assert isinstance(amend_result["corrections"], list)

            # Verify file was updated
            with open(target_path) as f:
                updated_content = f.read()
                assert "KEY::value2" in updated_content
                assert "value1" not in updated_content

    @pytest.mark.asyncio
    async def test_amend_with_base_hash_check(self):
        """Test base_hash consistency check."""
        create_tool = CreateTool()
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "test.oct.md")

            # Create initial file
            create_result = await create_tool.execute(
                content="===TEST===\nKEY::value1\n===END===",
                target_path=target_path,
            )
            original_hash = create_result["canonical_hash"]

            # Amend with correct base_hash
            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"KEY": "value2"},
                base_hash=original_hash,
            )
            assert amend_result["status"] == "success"

            # Amend with incorrect base_hash should fail
            amend_result2 = await amend_tool.execute(
                target_path=target_path,
                changes={"KEY": "value3"},
                base_hash="incorrect_hash",
            )
            assert amend_result2["status"] == "error"
            assert "errors" in amend_result2
            # Should mention hash mismatch
            assert any("hash" in str(err).lower() for err in amend_result2["errors"])

    @pytest.mark.asyncio
    async def test_amend_multiple_fields(self):
        """Test amending multiple fields at once."""
        create_tool = CreateTool()
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "test.oct.md")

            # Create initial file with multiple fields
            create_result = await create_tool.execute(
                content="===TEST===\nFIELD1::value1\nFIELD2::value2\nFIELD3::value3\n===END===",
                target_path=target_path,
            )
            assert create_result["status"] == "success"

            # Amend multiple fields
            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"FIELD1": "updated1", "FIELD3": "updated3"},
            )

            assert amend_result["status"] == "success"

            # Verify updates
            with open(target_path) as f:
                updated_content = f.read()
                assert "FIELD1::updated1" in updated_content
                assert "FIELD2::value2" in updated_content  # Unchanged
                assert "FIELD3::updated3" in updated_content

    @pytest.mark.asyncio
    async def test_amend_nonexistent_file_errors(self):
        """Test that amending nonexistent file returns error."""
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "nonexistent.oct.md")

            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"KEY": "value"},
            )

            assert amend_result["status"] == "error"
            assert "errors" in amend_result

    @pytest.mark.asyncio
    async def test_amend_returns_diff_by_default(self):
        """Test that compact diff is returned by default."""
        create_tool = CreateTool()
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "test.oct.md")

            # Create initial file
            await create_tool.execute(
                content="===TEST===\nKEY::value1\n===END===",
                target_path=target_path,
            )

            # Amend the file
            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"KEY": "value2"},
            )

            # Should have diff
            assert "diff" in amend_result

    @pytest.mark.asyncio
    async def test_amend_preserves_other_content(self):
        """Test that amend only changes specified fields."""
        create_tool = CreateTool()
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "test.oct.md")

            # Create file with complex structure
            initial_content = """===TEST===
META:
  VERSION::"1.0"
  STATUS::ACTIVE

CONFIG::production
TIMEOUT::30
===END==="""

            await create_tool.execute(
                content=initial_content,
                target_path=target_path,
            )

            # Amend only TIMEOUT
            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"TIMEOUT": 60},
            )

            assert amend_result["status"] == "success"

            # Verify other content preserved
            with open(target_path) as f:
                updated_content = f.read()
                assert "VERSION" in updated_content
                assert "STATUS::ACTIVE" in updated_content
                assert "CONFIG::production" in updated_content
                assert "TIMEOUT::60" in updated_content or "60" in updated_content

    @pytest.mark.asyncio
    async def test_amend_tracks_corrections(self):
        """Test that corrections are tracked when amending."""
        create_tool = CreateTool()
        amend_tool = AmendTool()

        with tempfile.TemporaryDirectory() as tmpdir:
            target_path = os.path.join(tmpdir, "test.oct.md")

            # Create initial file
            await create_tool.execute(
                content="===TEST===\nKEY::value1\n===END===",
                target_path=target_path,
            )

            # Amend with content that needs normalization
            amend_result = await amend_tool.execute(
                target_path=target_path,
                changes={"FLOW": "A -> B"},  # ASCII operator
            )

            # Should track corrections
            assert "corrections" in amend_result
            # May have ASCII normalization corrections

    @pytest.mark.asyncio
    async def test_amend_error_format(self):
        """Test error response format."""
        amend_tool = AmendTool()

        # Trigger error with invalid path
        amend_result = await amend_tool.execute(
            target_path="/invalid/../path.exe",
            changes={"KEY": "value"},
        )

        assert amend_result["status"] == "error"
        assert "errors" in amend_result
        assert isinstance(amend_result["errors"], list)

        # Errors should have structure
        if amend_result["errors"]:
            error = amend_result["errors"][0]
            assert "code" in error
            assert "message" in error
