//hovering the sidebar events

(function () {
    'use strict'
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
      new bootstrap.Tooltip(tooltipTriggerEl)
    })
  })()

// default function for rendering the data in div main

function renderData(data) {
    const mainDiv = document.querySelector('.main');
    mainDiv.innerHTML = data;
}

// geeting the dashboard data from flask when it click on the home button

function home() {
    // Make an AJAX request to fetch the data from Flask
    fetch('/home')
      .then(response => response.text())
      .then(data => {
        // Render the data in the div element
        renderData(data);
      });
    }

const homebtn = document.querySelector('#home-btn');
homebtn.addEventListener('click', () => {
    home();
});


// calling the home data using the home url using fetch ajax

function getData() {
    // Make an AJAX request to fetch the data from Flask
    fetch('/hirenow')
      .then(response => response.text())
      .then(data => {
        // Render the data in the div element
        renderData(data);
      });
    }


const hireNowBtn = document.querySelector('#hirenow-btn');
hireNowBtn.addEventListener('click', () => {
    getData();
});