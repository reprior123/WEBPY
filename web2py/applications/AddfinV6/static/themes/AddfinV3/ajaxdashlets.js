(function($){
	function handleAjaxResponse(response) {
		$(this.selector).parent().removeClass('loading');
		$('#dashlet_entire_' + this.id + ' .bd-center').html(response);
		ajaxCall = false;
	}
	
	function handleAjaxRequest() {
		$(this.selector).parent().addClass('loading');
		ajaxCall = $.ajax({
			type: "GET",
			url: this.url,
			data: {module: "AjaxDashlets", action: this.action, dashlet: this.dashlet, query_string: $(this.selector).val()}
		}).done(handleAjaxResponse.bind(this));
	}

	var ajaxCall = false, timeout = false;
	
	function handleKeyUp() {
		if (ajaxCall) {
			ajaxCall.abort();
			ajaxCall = false;
		}
		if ($(this.selector).val().length > 2) {
			clearTimeout(timeout);
			timeout = setTimeout(handleAjaxRequest.bind(this), 400);
		}
	}
	
	function handleRequestClearSearch(){
		$.ajax({
			type: "GET",
			url: this.url,
			data: {module: "Home", action: "DynamicAction", DynamicAction: "displayDashlet", session_commit: 1, to_pdf: 1, id: this.id}
		}).done(handleSearchAjaxResponse.bind(this));
	}
	
	function handleSearchAjaxResponse(resp){
		$('#dashlet_entire_' + this.id + ' .bd-center').html(resp);
		$('#dashlet_entire_' + this.id + ' .bd-center .hd').remove();
	}
	
	SUGAR.DashletAjaxSearch = function (obj) {
		$(obj.selector).keyup(handleKeyUp.bind(obj));
		$(obj.clearSelector).click(handleRequestClearSearch.bind(obj));
	};
})(jQuery);
