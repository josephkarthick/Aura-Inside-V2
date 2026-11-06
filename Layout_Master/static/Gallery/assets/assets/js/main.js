(function ($) {
	"use strict";

	$('.sidebar-button').on("click", function () {
		$(this).toggleClass('active');
	});

	document.querySelector('.sidebar-button').addEventListener('click', () =>
		document.querySelector('.main-menu').classList.toggle('show-menu'));

	$('.menu-close-btn').on("click", function () {
		$('.main-menu').removeClass('show-menu');
	});


	// Sidebar 
	$('.sidebar-btn').on("click", function () {
		$('.sidebar-area').addClass('active');
	});
	$('.sidebar-menu-close').on("click", function () {
		$('.sidebar-area').removeClass('active');
	});

	jQuery('.dropdown-icon').on('click', function () {
		jQuery(this).toggleClass('active').next('ul, .mega-menu, .mega-menu2').slideToggle();
		jQuery(this).parent().siblings().children('ul, .mega-menu, .mega-menu2').slideUp();
		jQuery(this).parent().siblings().children('.active').removeClass('active');
	});
	jQuery('.dropdown-icon2').on('click', function () {
		jQuery(this).toggleClass('active').next('.submenu-list').slideToggle();
		jQuery(this).parent().siblings().children('.submenu-list').slideUp();
		jQuery(this).parent().siblings().children('.active').removeClass('active');
	});


	//Counter up
	$('.counter').counterUp({
		delay: 10,
		time: 1500
	});


	// niceSelect
	$('select').niceSelect();

	// Home1 Banner Slider
	var swiper = new Swiper(".home1-banner-slider", {
		slidesPerView: 1,
		speed: 1500,
		effect: 'fade',
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		pagination: {
			el: ".swiper-pagination1",
			clickable: true,
		},
	});
	// Auction Slider
	var swiper = new Swiper(".home1-auction-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".auction-slider-next",
			prevEl: ".auction-slider-prev",
		},

		breakpoints: {
			280: {
				slidesPerView: 1,
			},
			386: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4,
				spaceBetween: 15,
			},
			1400: {
				slidesPerView: 4,
			},
		},
	});
	// General Slider
	var swiper = new Swiper(".home1-generat-art-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".generat-art-slider-next",
			prevEl: ".generat-art-slider-prev",
		},

		breakpoints: {
			280: {
				slidesPerView: 1,
			},
			386: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4,
				spaceBetween: 15,
			},
			1400: {
				slidesPerView: 4,
			},
		},
	});
	// Upcoming Auction Slider
	var swiper = new Swiper(".home1-upcoming-auction-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".upcoming-auction-slider-next",
			prevEl: ".upcoming-auction-slider-prev",
		},

		breakpoints: {
			280: {
				slidesPerView: 1,
			},
			386: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4,
				spaceBetween: 15,
			},
			1400: {
				slidesPerView: 4,
			},
		},
	});
	// Home1 Testimonial Slider
	var swiper = new Swiper(".home1-testimonial-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".testimonial-slider-next",
			prevEl: ".testimonial-slider-prev",
		},

		breakpoints: {
			280: {
				slidesPerView: 1,
			},
			386: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 2,
			},
			1200: {
				slidesPerView: 3,
				spaceBetween: 15,
			},
			1400: {
				slidesPerView: 3,
			},
		},
	});
	// Home1 Article Slider
	var swiper = new Swiper(".home1-article-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 25,
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".article-slider-next",
			prevEl: ".article-slider-prev",
		},

		breakpoints: {
			280: {
				slidesPerView: 1,
			},
			386: {
				slidesPerView: 1,
			},
			576: {
				slidesPerView: 1,
			},
			768: {
				slidesPerView: 2,
			},
			992: {
				slidesPerView: 3,
			},
			1200: {
				slidesPerView: 4,
				spaceBetween: 15,
			},
			1400: {
				slidesPerView: 4,
			},
		},
	});
	// Slick Slider
	$(".slider").slick({
		infinite: true,
		centerMode: false,
		arrows: true,
		dots: false,
		autoplay: true,
		autoplaySpeed: 2500,
		speed: 800,
		slidesToScroll: 1,
		vertical: true,
		verticalSwiping: true,
		slidesToShow: 2,
		slidesToScroll: 1,
		responsive: [{
			breakpoint: 1400,
			settings: {
				slidesToShow: 2
			}
		},
		{
			breakpoint: 1200,
			settings: {
				slidesToShow: 1
			}
		},
		{
			breakpoint: 992,
			settings: {
				slidesToShow: 1
			}
		}, {
			breakpoint: 768,
			settings: {
				arrows: false,
				slidesToShow: 1
			}
		}, {
			breakpoint: 576,
			settings: {
				arrows: false,
				slidesToShow: 1
			}
		}, {
			breakpoint: 480,
			settings: {
				arrows: false,
				vertical: false,
				verticalSwiping: false,
				slidesToShow: 1
			}
		}, {
			breakpoint: 350,
			settings: {
				arrows: false,
				vertical: false,
				verticalSwiping: false,
				slidesToShow: 1
			}
		}]
	});
	var swiper = new Swiper(".auction-details-nav-slider", {
		slidesPerView: 1,
		speed: 1500,
		spaceBetween: 15,
		grabCursor: true,
		autoplay: {
			delay: 2500, // Autoplay duration in milliseconds
			disableOnInteraction: false,
		},
		navigation: {
			nextEl: ".category-slider-next",
			prevEl: ".category-slider-prev",
		},
		breakpoints: {
			280: {
				slidesPerView: 2,
			},
			350: {
				slidesPerView: 3,
				spaceBetween: 10,
			},
			576: {
				slidesPerView: 4,
				spaceBetween: 15,
			},
			768: {
				slidesPerView: 5,
			},
			992: {
				slidesPerView: 5,
				spaceBetween: 15,
			},
			1200: {
				slidesPerView: 5,
			},
			1400: {
				slidesPerView: 5,
				spaceBetween: 35,
			},
		},
	});

	// var swiper = new Swiper(".auction-details-tab-swiper", {
	// 	slidesPerView: 1,
	// 	speed: 1500,
	// 	effect: 'fade',
	// 	autoplay: {
	// 		delay: 2500, // Autoplay duration in milliseconds
	// 		disableOnInteraction: false,
	// 	},
	// 	navigation: {
	// 		nextEl: ".auction-details-slider-next2",
	// 		prevEl: ".auction-details-slider-prev2",
	// 	},
	// });

		// Beauty Testimonial Slider
	
	const sliders = document.querySelectorAll('.auction-details-tab-swiper');
	sliders.forEach((slider) => {
		const nextBtn = slider.parentElement.querySelector('.auction-details-slider-next2');
		const prevBtn = slider.parentElement.querySelector('.auction-details-slider-prev2');

		const swiper = new Swiper(slider, {
			slidesPerView: 1,
			speed: 1500,
			spaceBetween: 10,
			loop: true,
			autoplay: false,
			effect: 'fade',
			navigation: {
				nextEl: nextBtn,
				prevEl: prevBtn,
			},
		});
		nextBtn.addEventListener('click', () => {
			swiper.slideNext();
		});

		prevBtn.addEventListener('click', () => {
			swiper.slidePrev();
		});
	});

	document.addEventListener("DOMContentLoaded", function (event) {

		let offset = 50;
		let circleContainer = document.querySelector(".circle-container");
		let circlePath = document.querySelector('.circle-container path');
		let pathLength = circlePath.getTotalLength();
		circlePath.style.transition = circlePath.style.WebkitTransition = 'none';
		circlePath.style.strokeDasharray = pathLength;
		circlePath.style.strokeDashoffset = pathLength;
		circlePath.getBoundingClientRect();
		circlePath.style.transition = circlePath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';

		let updateLoader = () => {

			let scrollTop = window.scrollY;
			let docHeight = document.body.offsetHeight;
			let winHeight = window.innerHeight;
			let height = docHeight - winHeight;
			let progress = pathLength - (scrollTop * pathLength / height);
			circlePath.style.strokeDashoffset = progress;

			if (scrollTop > offset) {
				circleContainer.classList.add("active");
			} else {
				circleContainer.classList.remove("active");
			}

		}
		circleContainer.onclick = function () {
			window.scrollTo({ top: 0, behavior: 'smooth' });
		}

		window.onscroll = () => {
			updateLoader();
		}
		updateLoader();
	});

	// Dark Light
	const dayNightSwitch = document.querySelector(".tt-style-switch");
	const darkModeButton = document.querySelector(".tt-style-switch .dark");
	const lightModeButton = document.querySelector(".tt-style-switch .light");

	const toggleDarkMode = (mode) => {
		const body = document.body;

		if (mode === "dark") {
			body.classList.add("dark");
			darkModeButton.classList.add("active");
			lightModeButton.classList.remove("active");
			localStorage.setItem("artmart_theme", "dark");
		} else {
			body.classList.remove("dark");
			lightModeButton.classList.add("active");
			darkModeButton.classList.remove("active");
			localStorage.removeItem("artmart_theme");
		}
	};

	// Event listeners for both buttons
	darkModeButton.addEventListener("click", () => toggleDarkMode("dark"));
	lightModeButton.addEventListener("click", () => toggleDarkMode("light"));

	// On page load, check the stored theme
	window.addEventListener("load", () => {
		const savedTheme = localStorage.getItem("artmart_theme");
		if (savedTheme === "dark") {
			toggleDarkMode("dark");
		} else {
			toggleDarkMode("light");
		}
	});

	const dayNight = document.querySelector(".dark-light-switch");
	dayNight.addEventListener("click", () => {
		dayNight.querySelector("i").classList.toggle("bi-brightness-low-fill");
		dayNight.querySelector("i").classList.toggle("bi-moon");
		document.body.classList.toggle("dark");

		var value = document.getElementById("body").className;
		var str = value;
		var last = str.split(" ").slice(-1)[0];
		if (last === "dark") {
			localStorage.setItem("artmart_theme", last);
		} else {
			localStorage.setItem("artmart_theme", "");
		}
		window.addEventListener("load", () => {
			if (document.body.classList.contains("dark")) {
				jQuery(".dark-light-switch i").addClass("bi bi-brightness-low-fill");
			} else {
				jQuery(".dark-light-switch i").addClass("bi bi-moon");
			}
		});
	});

	var artmart_theme = localStorage.getItem("artmart_theme");

	if (artmart_theme === "dark") {
		$("body").addClass("dark");
	}


	//Quantity Increment
	$(".quantity__minus").on("click", function (e) {
		e.preventDefault();
		var input = $(this).siblings(".quantity__input");
		var value = parseInt(input.val(),10);
		if (value > 1) {
			value--;
		}
		input.val(value.toString().padStart(2, "0"));
	});
	$(".quantity__plus").on("click", function (e) {
		e.preventDefault();
		var input = $(this).siblings(".quantity__input");
		var value = parseInt(input.val(),10);
		value++;
		input.val(value.toString().padStart(2, "0"));
	});


	// password-hide and show
	const togglePassword = document.querySelector('#togglePassword');
	const password = document.querySelector('#password');
	if (togglePassword) {
		togglePassword.addEventListener('click', function (e) {
			// toggle the type attribute
			const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
			password.setAttribute('type', type);
			// toggle the eye / eye slash icon
			this.classList.toggle('bi-eye');
		});
	}

	// New-password
	const togglePassword2 = document.getElementById('togglePassword2');
	const password2 = document.querySelector('#password2');
	if (togglePassword2) {
		togglePassword2.addEventListener('click', function (e) {
			// toggle the type attribute
			const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
			password2.setAttribute('type', type);
			// toggle the eye / eye slash icon
			this.classList.toggle('bi-eye');
		});
	}
	// confirm-password
	const togglePassword3 = document.getElementById('togglePassword3');
	const password3 = document.querySelector('#password3');
	if (togglePassword3) {
		togglePassword3.addEventListener('click', function (e) {
			// toggle the type attribute
			const type = password3.getAttribute('type') === 'password' ? 'text' : 'password';
			password3.setAttribute('type', type);
			// toggle the eye / eye slash icon
			this.classList.toggle('bi-eye');
		});
	}

	//wow js 
	jQuery(window).on('load', function () {
		new WOW().init();
		window.wow = new WOW({
			boxClass: 'wow',
			animateClass: 'animated',
			offset: 0,
			mobile: true,
			live: true,
			offset: 80
		})
		window.wow.init();
	});
	///Marquee
	const marquee = document.querySelectorAll(".marquee_text");
	if (marquee) {
		$(".marquee_text").marquee({
			direction: "left",
			duration: 25000,
			gap: 50,
			delayBeforeStart: 0,
			duplicated: true,
			startVisible: true,
		});
	}

	// Video Popup
	$('[data-fancybox="gallery"]').fancybox({
		buttons: [
			"close"
		],
		loop: false,
		protect: true
	});
	$('.video-player').fancybox({
		buttons: [
			"close"
		],
		loop: false,
		protect: true
	});

	// Language Btn
	$(".language-btn").on("click", function (e) {
		let parent = $(this).parent();
		parent.find(".language-list").toggleClass("active");
		e.stopPropagation();
	});
	$(document).on("click", function (e) {
		if (!$(e.target).closest(".language-btn").length) {
			$(".language-list").removeClass("active");
		}
	});

	// BTN Hover
	$(".btn-hover")
		.on("mouseenter", function (e) {
			var parentOffset = $(this).offset(),
				relX = e.pageX - parentOffset.left,
				relY = e.pageY - parentOffset.top;
			$(this).find("strong").css({ top: 0, left: 0 });
			$(this).find("strong").css({ top: relY, left: relX });
		})
		.on("mouseout", function (e) {
			var parentOffset = $(this).offset(),
				relX = e.pageX - parentOffset.left,
				relY = e.pageY - parentOffset.top;
			$(this).find("strong").css({ top: 0, left: 0 });
			$(this).find("strong").css({ top: relY, left: relX });
		});

	// timer start
	$("[data-countdown]").each(function () {
		var $deadline = new Date($(this).data("countdown")).getTime();
		var $dataDays = $(this).children("[data-days]");
		var $dataHours = $(this).children("[data-hours]");
		var $dataMinutes = $(this).children("[data-minutes]");
		var $dataSeconds = $(this).children("[data-seconds]");
		var x = setInterval(function () {
			var now = new Date().getTime();
			var t = $deadline - now;
			var days = Math.floor(t / (1000 * 60 * 60 * 24));
			var hours = Math.floor((t % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
			var minutes = Math.floor((t % (1000 * 60 * 60)) / (1000 * 60));
			var seconds = Math.floor((t % (1000 * 60)) / 1000);
			$dataDays.html(`${days} <span>D</span> <span>Days</span>`);
			$dataHours.html(`${hours} <span>H</span> <span>Hours</span>`);
			$dataMinutes.html(`${minutes} <span>M</span> <span>Minutes</span>`);
			$dataSeconds.html(`${seconds} <span>Sec</span> <span>Seconds</span>`);
			if (t <= 0) {
				clearInterval(x);
				$dataDays.html("00 <span>D</span> <span>Days</span>");
				$dataHours.html("00 <span>H</span> <span>Hours</span>");
				$dataMinutes.html("00 <span>M</span> <span>Minutes</span>");
				$dataSeconds.html("00 <span>Sec</span> <span>Seconds</span>");
			}
		}, 1000);
	});
	//list grid view
	$(".grid-view li").on("click", function () {
		// Get the class of the clicked li element
		var clickedClass = $(this).attr("class");
		// Extract the class name without "item-" prefix
		var className = clickedClass.replace("item-", "");
		// Add a new class to the target div and remove old classes
		var targetDiv = $(".list-grid-product-wrap");
		targetDiv.removeClass().addClass("list-grid-product-wrap " + className + "-wrapper");
		// Remove the 'selected' class from siblings and add it to the clicked element
		$(this).siblings().removeClass("active");
		$(this).addClass("active");
	});
}(jQuery));