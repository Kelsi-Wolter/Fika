"use strict";

// Add event listener to click on "create new list" button which redirects to /account/user_id/create_new_list

document.getElementById("new-list-btn").onclick = function () {
    location.href = '/create_new_list'      //need to be able to pass user id here??
    // alert('Hey!');
};