(function($) {
	
	var _data = {
		'notifications' : { }
	};

	SUGAR.Core = {
		updateNotifications: function(type, count) {
			_data.notifications[type] = parseInt(count);
			count = 0;
			for(type in _data.notifications) count += _data.notifications[type];
			Tinycon.setBubble(count);
		},
		init: function() {
			if(SUGAR.Core.hasOwnProperty($(this).attr('data-core'))) {
				SUGAR.Core[$(this).attr('data-core')].init(this);
			}
		},
		Table: {
			init: function(table) {
				table = $(table);
				table.find('.widget-sort-row:first a').click(SUGAR.Core.Table.update.bind(table));
				table.find('.pagination-buttons button').click(SUGAR.Core.Table.update.bind(table));
				table.find('table.table [class$=filters] input').on('click', SUGAR.Core.Table.filter.bind(table));
				table.find('table.table [class$=filters] .filters-selected').on('click', SUGAR.Core.Table.removeFilter.bind(table));
				table.find('table.table .clear-filters').on('click', SUGAR.Core.Table.removeAllFilters.bind(table));
				if(table.find('.mydashlet-search:first').size()) {
					table.find('.mydashlet-search:first .clear-search').on('click',SUGAR.Core.Table.clearSearch.bind(table));
					table.find('.mydashlet-search:first input').on('keyup', SUGAR.Core.Table.handleSearch.bind(table));
					table.find('.mydashlet-search:first .button').click(SUGAR.Core.Table.update.bind(table));
				}
				if(table.find('.filters ul.fancymenu').size()) {
					table.find('.filters ul.fancymenu').sugarActionMenu();
				}
				table.trigger('core:table_init');
			},
			filter: function(e) {
				var el = $(e.currentTarget);
				if(el.is('[data-multiple]')) {
					var filters = [], checkboxes = jQuery.unique(this.find('input[name="'+el.attr('name')+'"][type=checkbox]'));
					
					checkboxes.each(function(){
						if( $(this).is(':checked') ) {
							filters.push($(this).val());
						}
					});
					filters = jQuery.unique(filters);
					el.attr('data-params', el.attr('name') + '=' + filters.join('|'));
				} else if (el.is('[data-ignore]')) {
					return;
				} else {
					el.attr('data-params', el.attr('name') + '=' + el.val());
				}
				SUGAR.Core.Table.update.call(this, e);
			},
			clearSearch: function(e){
				var clearButton = $(e.currentTarget);
				clearButton.parent().find('.search-field').val("");
				SUGAR.Core.Table.update.call(this, e);
			},
			removeFilter: function(e){
				var input = $('#'+$(e.currentTarget).attr('for'));
				this.find('[name="' + input.attr('name') + '"][value="' + input.val() + '"]').removeAttr('checked').attr('disabled', true);
				this.find('[name="' + input.attr('name') + '"][type=hidden]').attr('disabled', true);
				e.currentTarget = input.get(0);
				SUGAR.Core.Table.filter.call(this, e);
				this.find('[name="' + input.attr('name') + '"][value="' + input.val() + '"], [name="' + input.attr('name') + '"][type=hidden]').removeAttr('disabled');
			},
			removeAllFilters: function(e){
				var el = $(e.currentTarget);
				var dataParams = [];
				var params = this.find('form [name^="filters["]').serializeArray();
				for(var i=0; i<params.length; i++) {
					if(params[i].name.indexOf("filters[")=== 0){
						dataParams.push(params[i].name + '=');
					}
				}
				el.attr('data-params', dataParams.join('&'));
				SUGAR.Core.Table.update.call(this, e);
			},
			update: function(e) {
				var dataParams = {};
				var params = this.find('form:first').serializeArray();
				for(var i=0; i<params.length; i++) {
					
					if(params[i].name in dataParams){
						if(dataParams[ params[i].name ].indexOf(params[i].value) == -1){
							dataParams[ params[i].name ] = params[i].value;
						}
					}else{
						dataParams[ params[i].name ] = params[i].value;
					}	
				}
				if(e && $(e.currentTarget).attr('data-params')) {
					var params = $(e.currentTarget).attr('data-params').split('&'), key, value;
					for(var i=0; i<params.length; i++) {
						key = params[i].substr(0, params[i].indexOf('='));
						value = params[i].substr(params[i].indexOf('=') + 1);
						if( value ) {
							dataParams[ key ] = value;
						} else {
							delete dataParams[ key ];
						}
					}
				}
				$(this).trigger('core:table_update');
				var url = 'index.php?' + $.param(dataParams);
				this.find('table').addClass('loading');
				this.data('promise', $.ajax(url, {success: SUGAR.Core.Table.handleSuccess.bind(this)}));
				ajaxStatus.showStatus(SUGAR.language.get('app_strings', 'LBL_LOADING'));
				e && e.preventDefault();
			},
			handleSuccess: function(data) {
				var container = this.parent();
				var focus = this.data('handle-focus');
				var previous = this.prev();
				this.remove();
				if(previous.size()) {
					previous.after(data);
				} else {
					container.append(data);
				}
				ajaxStatus.hideStatus();
				var tables = container.find('[data-core]');
				if(tables.size()) tables.each(SUGAR.Core.init);
				if(focus) {
					var el = tables.find(focus);
					var strLength = el.val().length;
					if(el.get(0).setSelectionRange !== undefined) {
						el.get(0).setSelectionRange(strLength, strLength);
					} else {
						$(el).val(el.value);
					}
				}
				$(tables).trigger('core:table_updated');
			},
			handleSearch: function(e) {
				if(this.data('promise')) {
					this.data('promise').abort();
					this.find('.mydashlet-search').removeClass('loading');
					this.data('promise','');
				}
				if(this.find('.mydashlet-search input').val().length > 1){
					clearTimeout(this.data('timeout'));
					this.data('timeout', setTimeout(SUGAR.Core.Table.handleSearchRequest.bind(this, e), 400));
				}
			},
			handleSearchRequest: function(e) {
				this.find('.mydashlet-search').addClass('loading');
				this.data('handle-focus', '.mydashlet-search input');
				var input = $(e.currentTarget);
				input.attr('data-params',input.attr('name') + '=' + encodeURIComponent(input.val()));
				SUGAR.Core.Table.update.call(this, e);
			}
		},
		Form:{
			init: function(form){
				form = $(form);
				if(form.find("button[type='submit']").size() <= 0)
					form.find('input, select, textarea').on('change', SUGAR.Core.Form.submitForm.bind(form));
			},
			getFormData: function() {
				var params = {};
				this.find('input, select, textarea').each(function(){
					params[$(this).attr('name')] = $(this).val();
				});
				return params;
			},
			submitForm: function(e){
				var params = SUGAR.Core.Form.getFormData.call(this);
				this.find('input, select, textarea').attr("disabled","disabled");
				$.ajax({
					type: this.is('form') ? this.attr('method') : this.attr('data-method'),
					url: this.is('form') ? this.attr('action') : this.attr('data-action'),
					data: params,
					success: SUGAR.Core.Form.handleSuccess.bind(this),
					error: SUGAR.Core.Form.handleError.bind(this),
				});
				ajaxStatus.showStatus(SUGAR.language.get('app_strings', 'LBL_LOADING'));
			},
			handleSuccess: function(e){
				this.find('input, select, textarea').removeAttr('disabled');
				ajaxStatus.hideStatus();
			},
			handleError: function(e){
				this.find('input, select, textarea').removeAttr('disabled');
				ajaxStatus.hideStatus();
			}
		}
				
		
	};

	$(function(){
		$.each(SUGAR.Core, function(c) {
			if(c[0] === c[0].toUpperCase()) {
				$(document).on('core:init_' + c.toLowerCase(), function(e){
					if(e.target && $(e.target).is('[data-core]') && SUGAR.Core[c].init) {
						SUGAR.Core[c].init($(e.target));
					}
				});
			}
		});

		$('[data-core]').each(SUGAR.Core.init);
	});
}(jQuery));