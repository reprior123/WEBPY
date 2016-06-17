(function ($) {
	SUGAR.DatabaseProductsMetadata = {
		updateProduct: function(productId){
			$.ajax({
				url: 'index.php',
				data: {module: 'DatabaseProducts', action: 'updateProduct', id: productId},
				complete: function(){
					SUGAR.Core.Table.update.call($("#database-table"));
					$.colorbox.close();
				}
			});
		},
		openMetadata: function(listingKey){
			$.colorbox({width:'900', height:'580', rel: false, href: '/index.php?module=DatabaseProductsMetadata&action=showData&id=' + listingKey});
		},
		modifyInputValue: function(e){
			var name = $(e.currentTarget).attr('name');
			$(".metadata-overlay [name='"+name+"']").attr("value",$(e.currentTarget).val());
		},
		saveData: function(id){
			var input_array = $('.metadata-overlay input:not(.metadata-overlay form input)'), select_array = $('.metadata-overlay select'), data = {};
			input_array.each(function(){
				if($(this).attr('type') == 'checkbox'){
					($(this).is(':checked')) ? data[$(this).attr('name')] = true : data[$(this).attr('name')] = false ;
				}else{
					data[$(this).attr('name')] = $(this).val();
				}
				
			});
			
			select_array.each(function(){
				data[$(this).attr('name')] = $(this).val();
			});
			$.ajax({
				type: "POST",
				url:'index.php?module=DatabaseProducts&action=saveData&id='+id,
				data: data,
				complete: function(){
					SUGAR.Core.Table.update.call($("#database-table"));
					$.colorbox.close();
				}
			});
		}
	};
})(jQuery);

