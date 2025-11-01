// Get all modal elements and close buttons
const modals = document.querySelectorAll(".modal");
const closeButtons = document.querySelectorAll(".close-button");

// Get all the buttons that open the modals
const openButtons = document.querySelectorAll(".ui.button");

openButtons.forEach((button) => {
  button.addEventListener("click", () => {
    // Get the target modal id from the button's data-target attribute
    const targetModalId = button.getAttribute("data-target");
    const targetModal = document.getElementById(targetModalId);

    // Show the corresponding modal
    targetModal.showModal();
  });
});

// Close the modals when clicking the "Close" button
closeButtons.forEach((button) => {
  button.addEventListener("click", () => {
    // Close the modal containing the close button that was clicked
    const modal = button.closest(".modal");
    modal.close();
  });
});
