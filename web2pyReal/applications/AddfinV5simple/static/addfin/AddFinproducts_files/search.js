(function($) {
	
	var isOver = false;
	var timeout = false;
	var promise = false;
	var container = $('.quick-search-wrapper'), 
		results = $(".autocompleted-list");
	
	function shouldShowSearch( e ) {
		if( e.type === 'mouseleave' ) isOver = false;
		if(!container.find("input").is(':focus') && !isOver) {
			container.removeClass("focused");
			results.stop(true).delay(200).slideUp();
		}
	}

	function handleAjaxRequest() {
		container.addClass('loading');
		results.stop(true).slideUp();
		promise = $.ajax({
			type: "GET",
			url: "index.php",
			data: { module: "AjaxSearch", action: "AjaxSearch", search_form: "false", advanced: "false", query_string: container.find('input').val() }
		}).done(handleAjaxResponse);
	}

	function handleAjaxResponse(response){
		container.removeClass('loading');
		if(!results.is(':visible')){
			results.show();
		}
		results.html(response);
		results[results.height() < container.find(".search-united").height() ? 'addClass' : 'removeClass' ]("scroll");
		results.stop(true).hide().slideDown();
		promise = false;
	}
	
	function handleInputFocus() {
		var el = container.find("input" );
		var strLength = el.val().length;
		if(el.get(0).setSelectionRange !== undefined) {
			el.get(0).setSelectionRange(0, strLength);
		} else {
			$(el).val(el.value);
		}
	}
	
	$(function() {
		container.find("input").focus(function() {
			isOver = true;
			container.addClass("focused");
			setTimeout(handleInputFocus, 5);
		}).blur(shouldShowSearch);
		container.mouseleave(shouldShowSearch);
		
		container.find("input").on('keyup', function(){
			if( promise ) {
				promise.abort();
				container.removeClass('loading');
				promise = false;
			}
			if(this.value.length > 2){
				clearTimeout(timeout);
				timeout = setTimeout(handleAjaxRequest, 400);
			}
		});
	});
}(jQuery));