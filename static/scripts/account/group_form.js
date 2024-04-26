$(document).ready(function () {
  $("#delete-btn").attr("disabled", "disabled");
  $("#id_permissions option").each(function () {
    if ($(this).is(":selected")) {
      $("#selected_permissions").append(
        $("<option>", {
          value: $(this).val(),
          text: $(this).text(),
        })
      );
    }
  });
  $("#id_permissions").change(function (e) {
    e.preventDefault();

    $("#selected_permissions").children().remove();

    $("#id_permissions option").each(function () {
      if ($(this).is(":selected")) {
        $("#selected_permissions").append(
          $("<option>", {
            value: $(this).val(),
            text: $(this).text(),
          })
        );
      }
    });
  });

  $("#id_permissions option").each(function () {
    $(this).attr("data-search-term", $(this).text());
  });

  $("#live-search").on("keyup", function () {
    var searchTerm = $(this).val();

    $("#id_permissions option").each(function () {
      if (
        $(this).filter("[data-search-term *= " + searchTerm + "]").length > 0 ||
        searchTerm.length < 1
      ) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
});
