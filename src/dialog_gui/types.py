from typing import List, Literal, TypedDict, Union, Any, Callable, Optional, Dict, NotRequired, Unpack


# Type hints for dialog ui

class OptionItem(TypedDict):
    value: str

    data: NotRequired[Any] # what you want returned from option when selected
    selected: NotRequired[bool]
    # orphan: NotRequired[bool] # This is a random field that I registered for my callback but you can have any field here for your needs

class InputField(TypedDict):
    form_field: Literal['input']
    label: str

    # optional
    type: NotRequired[Literal['text', 'password']]
    default: NotRequired[Any]
    disabled: NotRequired[bool]
    hide: NotRequired[List[str]]

class ListboxField(TypedDict):
    form_field: Literal['listbox']
    label: str
    info: List[OptionItem]

    multiple: NotRequired[bool]
    disabled: NotRequired[bool]
    hide: NotRequired[List[str]]
    # callback: NotRequired[Callable[..., Any]]

class ComboboxField(TypedDict):
    form_field: Literal['combobox']
    label: str
    info: List[OptionItem]

    default: NotRequired[Any]
    disabled: NotRequired[bool]
    hide: NotRequired[List[str]]
    callback: NotRequired[Callable[..., Any]]

FormField = Union[InputField, ListboxField, ComboboxField]

FormConfiguration = List[FormField]

# Helper functions to create correct input fields
def option(value: str, selected=False, **kwargs: Any) -> OptionItem:
    return {'value': value, 'selected': selected, **kwargs} # type: ignore

def input_field(label: str,
                type: Literal['text', 'password'] = 'text',
                default: Any = None,
                disabled: bool = False,
                hide: Optional[List[str]] = None,
                **kwargs: Any
                ) -> InputField:
    # Note: 'Unpack' requires Python 3.11+. For older versions, just use **kwargs
    # and simple dict construction.
    return {'form_field': 'input', 'label': label, 'type': type, 'default': default, 'disabled': disabled, 'hide': hide, **kwargs}  # type: ignore

def combobox_field(label: str, info: List[OptionItem], disabled=[], hide=[], default=None, callback=None, **kwargs: Any) -> ComboboxField:
    return {'form_field': 'combobox', 'label': label, 'info': info, 'default': default, 'disabled': disabled, 'hide': hide, 'callback': callback, **kwargs} # type: ignore

def listbox_field(label: str, info: List[OptionItem], multiple=True, disabled=[], hide=[], **kwargs: Any) -> ListboxField:
    return {'form_field': 'listbox', 'label': label, 'info': info, 'multiple': multiple, 'disabled': disabled, 'hide': hide, **kwargs} # type: ignore