document.addEventListener("DOMContentLoaded", function () {
  // Toggle switch functionality
  const toggleSwitch = document.querySelector("#hashtags");
  toggleSwitch.addEventListener("change", function () {
    // Add any specific functionality for the hashtags toggle
    console.log("Hashtags enabled:", this.checked);
  });

  // User/Admin toggle functionality
  const userToggleBtns = document.querySelectorAll(".user-toggle .toggle-btn");
  userToggleBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      userToggleBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");
    });
  });

  // Price tag toggle functionality
  const priceTags = document.querySelectorAll(".price-tag");
  priceTags.forEach((tag) => {
    tag.addEventListener("click", function () {
      priceTags.forEach((t) => t.classList.remove("active"));
      this.classList.add("active");
    });
  });

  // Generate post button functionality
  const generateBtn = document.querySelector(".generate-btn");
  generateBtn.addEventListener("click", function () {
    // Add generation functionality here
    console.log("Generating post...");

    // Get form values
    const productTopic = document.querySelector(
      'input[placeholder="Add a product, event, campaign"]'
    ).value;
    const description = document.querySelector("textarea").value;
    const language = document.querySelector("select").value;
    const zipcode = document.querySelector(
      'input[placeholder="Add a zipcode"]'
    ).value;
    const companyName = document.querySelector(
      'input[placeholder="Add company name"]'
    ).value;
    const companyWebsite = document.querySelector(
      'input[placeholder="Add company website"]'
    ).value;

    // Example of collecting form data
    const formData = {
      productTopic,
      description,
      language,
      zipcode,
      includeHashtags: toggleSwitch.checked,
      companyName,
      companyWebsite,
    };

    console.log("Form data:", formData);
    // Here you would typically send this data to your backend
  });

  // Add input field focus effects
  const inputFields = document.querySelectorAll(
    ".input-field input, .input-field textarea"
  );
  inputFields.forEach((field) => {
    field.addEventListener("focus", function () {
      this.parentElement.style.outline = "2px solid rgb(37 99 235)";
    });

    field.addEventListener("blur", function () {
      this.parentElement.style.outline = "none";
    });
  });
});
