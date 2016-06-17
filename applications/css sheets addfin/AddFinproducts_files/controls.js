(function($){
	var settings = {
		'textOn' : 'ON',
		'textOff' : 'OFF'
	};
	var documentBlur = function(e){
		$('.focus[data-control]').each(function(){
			if( $(e.target).closest('[data-control]').get(0) !== this ) {
				$(this).data('control').blur();
			}
		});
	};
	
	var Abstract = {
		focus: function() {
			this.container.addClass('focus');
			$(document).on('click', documentBlur);
			this.update();
		},
		blur: function(){
			this.container.removeClass('focus');
			$(document).off('click', documentBlur);
			this.update();
		},
		contextEval: function(string) {
			return eval(string);
		},
		update: function() {}
	};
	
	var Checkbox = function( input ) {
		this.input = $(input);
		this.init();
	};
	Checkbox.prototype = $.extend({}, Abstract, {
		init: function() {
			this.container = $('<span>').addClass(this.input.attr('class') + ' icon').attr('data-control','checkbox');
			this.container.data('control', this);
			this.input.before(this.container);
			this.input.change(this.update.bind(this));
			this.container.append(this.input.hide());
			this.container.click(this.focus.bind(this));
			this.update();
		},
		focus: function() {
			if( this.input.prop("disabled") ) return;
			var checked = this.input.prop("checked");
			this.input.prop("checked", !checked);
			Abstract.focus.call(this);
			if(this.input.attr('onclick')) {
				this.contextEval.call(this.input.get(0),this.input.attr('onclick'));
			}
		},
		update: function() {
			this.container.toggleClass('checked', this.input.is(':checked'));
			this.container.toggleClass('disabled', this.input.is(':disabled'));
		}
	});

	var Checkable = function( input ) {
		this.input = $(input);
		this.init();
	};
	Checkable.prototype = $.extend({}, Checkbox.prototype, {
		init: function() {
			this.container = $('<span>').addClass(this.input.attr('class')).attr('data-control','');
			this.container.data('control', this);
			this.input.before(this.container);
			this.container.append($('<span class="switch-on"><span>'+settings.textOn+'</span></span>'+
				'<span class="switch-off"><span>'+settings.textOff+'</span></span>'+
				'<span class="switch-button"></span>'));
			this.container.append(this.input.hide());
			this.container.addClass(this.input.is(':checked') ? 'checked' : '');
			this.container.click(this.focus.bind(this));
			this.update();
		}
	});

	var Selectable = function( input ) {
		this.input = $(input);
		this.init();
	};
	Selectable.prototype = $.extend({}, Abstract, {
		init: function() {
			this.container = $('<span>').addClass(this.input.attr('class')).attr('data-control','');
			this.container.data('control', this);
			this.input.before(this.container);
			this.container.append($('<span class="select-value"></span>'+
				'<span class="select-arrow"></span>'+
				'<span class="drop-down"></span>'));
			this.container.append(this.input.hide());
			this.container.find('.select-value, .select-arrow').click(this.focus.bind(this));
			var dropDown = this.container.find('.drop-down');
			this.input.find('option').each(function(){
				dropDown.append($('<span>').addClass($(this).is(':selected') ? 'selected' : '').attr('data-value', $(this).val()).text($(this).text()));
			});
			dropDown.on('click', 'span[data-value]', this.handleSelect.bind(this));
			this.update();
		},
		focus: function(){
			Abstract[ this.container.hasClass('focus') ? 'blur' : 'focus'].call(this);
		},
		handleSelect: function(e) {
			this.input.val( $(e.target).attr('data-value') ).change();
			this.update();
			this.blur();
		},
		update: function() {
			this.container.find('.select-value').text(this.input.find('option:selected').text());
		}
	});
	
	
	$('input.switch').each(function(){
		new Checkable(this);
	});
	$('select.select').each(function(){
		new Selectable(this);
	});
	$('input.checkbox').each(function(){
		new Checkbox(this);
	});
})(jQuery);
