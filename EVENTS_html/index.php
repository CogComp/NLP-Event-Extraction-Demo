<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="PRAGMA" CONTENT="NO-CACHE">
    <META HTTP-EQUIV="EXPIRES" CONTENT="0">
    <title>Event Extraction Demo (2020)</title>
    <link rel="stylesheet" type="text/css" href="./html/w3.css">
    <link rel="stylesheet" type="text/css" href="./html/events.css">
	<script src="./html/jquery-3.5.1.min.js"></script>
	<script src="./html/events.js"></script>
    <style>
    </style>
</head>
<body>
<div class="main">
	<form id="demoForm" name="demoForm" onSubmit="return false;">
		<div class="w3-container">
			<div class="w3-left">
				<label> <b>Annotators</b> </label>
				<br>
				<!-- 
				<input class="w3-check annotator" type="checkbox" checked="checked" id="NER">
				<label class="container">NER</label>
				<label class="container">&nbsp;</label>
				<input class="w3-check annotator" type="checkbox" checked="checked" id="SRL">
				<label class="container">SRL</label>
				<label class="container">&nbsp;</label>
				-->
				<input class="w3-check annotator" type="checkbox" checked="checked" id="EVENTS" disabled="true">
				<label class="container">EVENTS</label>
				<label class="container">&nbsp;</label>

				<input class="w3-check annotator" type="checkbox" checked="checked" id="TEMPORAL">
				<label class="container">Temporal</label>
				<label class="container">&nbsp;</label>
				
				<input class="w3-check annotator" type="checkbox" checked="checked" id="STORYLINE">
				<label class="container">Coref</label>
				<label class="container">&nbsp;</label>

			</div>
			<div class="w3-right">
				<label> <b>Examples:</b> </label>
				<br>
				<select class="w3-select w3-border" id="example" name="example" value="" onChange="javascript:newExampleSelect();" style="width:512px;">
					<!--<option value="">Select a language... -->
				</select>
			</div>
		</div>
		<div class="w3-container">
			<label> <b>Text:</b> </label>
			<br>
			<textarea class="w3-input w3-border" id="text" name="text" rows="4" cols="50" style="resize: vertical;"></textarea>
		</div>
		<div class="w3-container">
			<button class="w3-button w3-blue" onClick="return formSubmit();"> Run > </button>
		</div>
	</form>

	<!--<div class="w3-container">-->
		&nbsp;
		<br>
		<div id="result" class="w3-container">
		</div>
	<!--</div>-->

</div>

<script>main();</script>
</body>
</html>
