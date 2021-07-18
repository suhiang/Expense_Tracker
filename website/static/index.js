function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteCategory(categoryId) {
  fetch("/delete-category", {
    method: "POST",
    body: JSON.stringify({ categoryId: categoryId }),
  }).then((_res) => {
    window.location.href = "/categories";
  });
}

function deleteExpense(expenseId) {
  fetch("/delete-expense", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}