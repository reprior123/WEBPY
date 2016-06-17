(function ($) {
	var defaultTimeout = 300;
	var timeout = {};
	var currentLevel1 = $;

	function mouseEnterDeffered() {
		$(this).addClass('open').parent().addClass('large-ul');

	}
	function mouseEnter() {
		if (!$(this).hasClass('locked')) {
			clearTimeout(timeout[$(this).attr('class')]);
			timeout[$(this).attr('class')] = setTimeout(mouseEnterDeffered.bind(this), defaultTimeout);
		}
	}
	function mouseLeaveDeffered() {
		$(this).removeClass('open').parent().removeClass('large-ul');
	}
	function mouseLeave() {
		if (!$(this).hasClass('locked')) {
			clearTimeout(timeout[$(this).attr('class')]);
			timeout[$(this).attr('class')] = setTimeout(mouseLeaveDeffered.bind(this), defaultTimeout);
		}
	}

	function showCurrent() {
		var url = $(location).attr('href'),
				link = (url.substring(url.lastIndexOf("/") + 1, url.length) != '') ? url.substring(url.lastIndexOf("/") + 1, url.length) : 'index.php',
				current = $('nav.main a[href="' + link + '"]'),
				current_module = getCurrentModule('module'),
				arr = $('nav.main a[href*="module=' + current_module + '"]');
		if (current.size()) {
			var current = current.closest('li');
			while (current.size() > 0) {
				current.addClass('current');
				current = current.parent().closest('li');
			}
		}
		
		if(arr && !current.size()) {
			for(var i = 0; i < arr.length -1; i++){
				if($(arr[i]).hasClass('primary')){
					current = $(arr[i]).closest('li');
					current.addClass('current');
				}
			}
		}
	}

	function getCurrentModule(variable) {
		var query = window.location.search.substring(1),
			vars = query.split("&");
		for (var i = 0; i < vars.length; i++) {
			var pair = vars[i].split("=");
			if (pair[0] == variable) {
				return pair[1];
			}
		}
		return false;

	}

	function toggleCookie() {
		if ($.cookie('submenu') === undefined || $.cookie('submenu') === 'collapsed') {
			$.cookie('submenu', 'expanded');
		} else {
			$.cookie('submenu', 'collapsed');
		}
		updateSubmenu();
	}

	function updateSubmenu() {
		if ($.cookie('submenu') == 'expanded') {
			currentLevel1.addClass('locked');
			$('section.main').addClass('main-open');
			$('section.main').removeClass('main-submenu');
		} else {
			currentLevel1.removeClass('locked');
			$('section.main').addClass('main-submenu');
			$('.level1').removeClass('large-ul');
			$('section.main').removeClass('main-open');
		}
	}

	currentLevel1 = $('nav.main .level1 > li.current');
	$('nav.main li.locked-animation').removeClass('locked-animation');
	if (currentLevel1.size() && currentLevel1.find('ul').size()) {
		$("section.main #content").prepend('<div class="submenu-bar"><div class="expand-wrapper"><a href="javascript:void(0)" class="btn-expand"></a></div></div>');
		updateSubmenu();
	}
	
	$(function () {
		$('nav.main .level1 > li').mouseenter(mouseEnter).mouseleave(mouseLeave);
		$('.submenu-title > .collapse-link').click(function () {
			toggleCookie();
			$(this).closest('li.current').removeClass('open').parent().removeClass('large-ul');
		});
		$('section.main .btn-expand').click(function () {
			toggleCookie();
		});

		if ($('nav.main ul.level2 li').hasClass('current')) {
			$('nav.main ul.level2 li.current').children('ul.level3').show();
			if($('nav.main ul.level2 li.current').hasClass('accordion-item')) $('nav.main ul.level2 li.current').addClass('expanded');
		}

		var accordionItems = $('nav.main ul.level3');
		$("nav.main ul.level2 > li.accordion-item").click(function (e) {
			if (!$(e.target).hasClass('accordion-item'))
				return;

			if(!$(e.target).hasClass('expanded')) {
				accordionItems.slideUp();
				$(this).children('ul.level3').stop(true).slideDown();
				$("nav.main ul.level2 > li.accordion-item").removeClass('expanded');
				$(e.target).addClass('expanded');
			}
			
			else {
				$(this).children('ul.level3').stop(true).slideUp();
				$("nav.main ul.level2 > li.accordion-item").removeClass('expanded');
			}
		});
	});
}(jQuery));
