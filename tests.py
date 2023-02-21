import pytest
import mock
import pdb_tools

test = "testtest"
test_file = "test1 \ntest2 \ntest3 \n"

#@mock.patch("builtins.open", new_callable=mock.mock_open, read_data=test_file)
#def test_read_line(open_fn):
#    f = open(test, 'r')
#    print(f)
#    return

#def test_split_segment():
#    #given
#    pdb_file, segname, pdb_id = "test.pdb", "ACHA", "3HB3"
#    #when
#    pdb_tools.operations.split_segment(pdb_file=pdb_file, segname=segname, pdb_id=pdb_id)
#    #then

@pytest.mark.parametrize("test_input,expected_output", [(1,"    1"), (10, "   10"), (100, "  100"), (1000, " 1000"), (99999, "99999")])
def test_fill_serial(test_input, expected_output):
    line_dict = {}
    line_dict = pdb_tools.lines.fill_serial(serial_no=test_input, line_dict=line_dict)
    assert line_dict["serial_no"] == expected_output

def test_fill_serial_fail():
    serial_no, line_dict = 100000, {}
    with pytest.raises(ValueError) as error: #works like try catch but puts error into variable so we can test for error (smth. like that)
        line_dict = pdb_tools.lines.fill_serial(serial_no=serial_no, line_dict=line_dict)
    assert error.type == ValueError

def test_filter_segment():
    lines, segname = ["ACHA", "BCHA"], "ACHA"
    filtered_lines = pdb_tools.operations._filter_segment(lines=lines, segname=segname)
    assert filtered_lines == ["ACHA"]