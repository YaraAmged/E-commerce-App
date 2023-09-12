const prefillInputs = () => {
  const url = window.location.search;
  const urlParams = new URLSearchParams(url);
  if (url.length < 2) return;
  console.log(url);
  document.querySelectorAll("select").forEach((input) => {
    const value = urlParams.get(input.name);
    const options = input.querySelectorAll("option");
    options.forEach((option) => {
      if (option.value == value) option.selected = true;
    });
  });
  document.querySelectorAll("input").forEach((input) => {
    const value = urlParams.get(input.name);
    switch (input.type) {
      case "radio":
        if (input.value == value) input.checked = true;
        break;
      default:
        input.value = value;
    }
  });
  const searchKeyword = urlParams.get("searchKeyword");
  if (searchKeyword) {
    const form = document.querySelector("#products-filters");
    if (!form) return;
    const hiddenInput = document.createElement("input");
    hiddenInput.hidden = true;
    hiddenInput.name = "searchKeyword";
    hiddenInput.value = searchKeyword;
    form.appendChild(hiddenInput);
  }
};
prefillInputs();
