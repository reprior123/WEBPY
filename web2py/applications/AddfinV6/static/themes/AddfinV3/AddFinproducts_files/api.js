(function($){

	function init(e) {
		var t = $(e.target);
		if(t.hasClass('alfresco-documents-wrapper')) {
			t.find('ul.fancymenu').sugarActionMenu();
			t.find('.wrapper table [data-params]').click(SUGAR.Core.Table.update.bind(t));
		}
	}

	function upload(e) {
		var form = $(e).closest('[data-core]').find('form');
		var url = '/index.php?action=upload&' + form.serialize();
		form.ajaxSubmit({
			url: url,
			type: 'post',
			success: SUGAR.Core.Table.handleSuccess.bind(form.closest('[data-core]'))
		});
	}

	function deleteNode(e) {
		if( confirm('Are you sure you want to delete object ' + $(e).attr('value') + ' ?') ) {
			var form = $(e).closest('form');
			var url = '/index.php?action=deleteNode&' + form.serialize() + '&' + $(e).attr('name') + '=' + $(e).attr('value');
			$.get(url, SUGAR.Core.Table.handleSuccess.bind(form.closest('[data-core]')), 'html');
		}
		return false;
	}

	$(document).on('core:table_init', init);
	
	top.AlfrescoAPI = {
		deleteNode: deleteNode,
		upload: upload
	};
})(jQuery);
