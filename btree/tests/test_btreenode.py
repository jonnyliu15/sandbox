from btree.btree import BTreeNode, BTreeNodeType
from btree.uint64 import uint64
import pytest


def test_btree_node_header():

    node = BTreeNode()
    node.set_header(BTreeNodeType.INTERNAL, 10)

    assert BTreeNodeType(node.type) == BTreeNodeType.INTERNAL
    assert node.number_of_keys == 10


def test_btree_node_ptr():
    node = BTreeNode()
    ptr = uint64(10)
    node.set_header(BTreeNodeType.LEAF, 2)

    node.set_ptr(0, ptr)
    assert node.get_ptr(0).value == 10

    node.set_ptr(1, ptr)
    assert node.get_ptr(0).value == 10

    assert node.get_ptr(1).value == 10
    node.set_ptr(0, ptr)

    with pytest.raises(AssertionError):
        node.set_ptr(2, ptr)


def test_btree_node_offset():
    node = BTreeNode()
    offset = 10
    node.set_header(BTreeNodeType.LEAF, 2)
    with pytest.raises(AssertionError):
        node.set_offset(0, offset)

    node.set_offset(1, offset)
    assert node.get_offset(0) == 0

    assert node.get_offset(1) == 10

    with pytest.raises(AssertionError):
        node.set_offset(2, offset)
