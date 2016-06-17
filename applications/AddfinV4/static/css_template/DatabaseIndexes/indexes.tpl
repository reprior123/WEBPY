<div class='moduleTitle moduleTitle_bigger'>
	<h2>{$MOD.LBL_INDICES_BREADCRUMB_SECTION} &raquo; {$MODS.LBL_MODULE_TITLE}</h2>
</div>
<div class="clearfix"></div>
{sugar_custom_call class="DatabaseIndexes_View_Table" method="render"}
<div class="disclaimer">{$APP.LBL_DISCLAIMER}</div>
{literal}
<script type="text/javascript">
	(function(){
		SUGAR.DbIndexes = {
			openColorbox: function(e) {
					$(e.currentTarget).colorbox({width:'900', height:'580', rel: false});					
				}
		}
		
	})();
</script>
{/literal}
{include file="modules/Database/tpls/js.tpl"}