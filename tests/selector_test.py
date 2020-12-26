import sys
sys.path.append('../')


from liquidcss.selectors import SelectorManager


def test_generate_uuid(selector_manager):
    id_ = selector_manager._generate_uuid()
    assert(isinstance(id_, str))
    assert(id_[0].isalpha())
    


if __name__ == "__main__":
    selector_manager = SelectorManager(base_dir = os.getcwd())
    test_generate_uuid(selector_manager)