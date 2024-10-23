$(document).ready(function () {
  $(".add-to-selection").on("click", function () {
    let button = $(this);
    let id = button.attr("data-index");
    // console.log(id);

    let hotel_id = $("#id").val();
    let room_id = $(`.room_id_${id}`).val();
    let hotel_name = $("#hotel_name").val();
    let room_name = $("#room_name").val();
    let room_type = $("#room_type").val();
    let room_price = $("#room_price").val();
    let number_of_beds = $("#number_of_beds").val();
    let checkin = $("#checkin").val();
    let checkout = $("#checkout").val();
    let adult = $("#adult").val();
    let children = $("#children").val();

    console.log(hotel_id);
    console.log(room_id);
    console.log(room_number);
    console.log(hotel_name);
    console.log(room_name);
    console.log(room_type);
    console.log(room_price);
    console.log(number_of_beds);
    console.log(checkin);
    console.log(checkout);
    console.log(adult);
    console.log(children);

    $.ajax({
      url: "/booking/add_to_selection/",
      data: {
        id: id,
        hotel_id: hotel_id,
        room_id: room_id,
        hotel_name: hotel_name,
        room_name: room_name,
        room_type: room_type,
        room_price: room_price,
        number_of_beds: number_of_beds,
        checkin: checkin,
        checkout: checkout,
        adult: adult,
        children: children,
      },
      dataType: "json",
      beforeSend: function () {
        console.log("sending data to server...");
      },
      success: function (response) {
        console.log(response);
      },
    });
  });
});

//delete item
$(document).on("click", ".delete-item", function () {
  let id = $(this).attr("data-item"); // Corrected attribute name
  let button = $(this);

  $.ajax({
    url: "/booking/delete_selection/",
    method: "GET",
    data: {
      id: id,
    },
    dataType: "json",
    beforeSend: function () {
      button.html("<i class='fas fa-spinner fa-spin'></i>");
    },
    success: function (response) {
      console.log(response);
      if (response.success) {
        // Remove the deleted item from the UI
        button.closest(".room-info").remove();
      } else {
        // Handle deletion failure
        console.error("Deletion failed:", response.message);
      }
    },
    error: function (xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText); // Log any errors for debugging
    },
  });
});
// end of delete on booking

//button-goes-to selected items
document.addEventListener("DOMContentLoaded", function () {
  const checkoutButton = document.getElementById("checkout-button");
  if (checkoutButton) {
    checkoutButton.addEventListener("click", function () {
      const selectedRoomsUrl = "{% url 'selected_rooms/' %}";
      window.location.href = selectedRoomsUrl;
    });
  }
});
