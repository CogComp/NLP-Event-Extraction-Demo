var xel_examples = {
    "eng": [
		"The eruption of an underwater volcano near Tonga on Saturday was likely the biggest recorded anywhere on the planet in more than 30 years, according to experts. Dramatic images from space captured the eruption in real time, as a huge plume of ash, gas and steam was spewed up to 20 kilometers into the atmosphere and tsunami waves were sent crashing across the Pacific." ,
		"Crews fighting a massive fire along the central coast of California near the iconic Highway 1 made progress Sunday in containing the blaze, but dozens of homes remained under evacuation orders. The Colorado fire ignited Friday evening in Palo Colorado Canyon in the Big Sur region of Monterey County and swelled to 1050 acres Saturday, up from 100 acres a day prior." , 
		"At least seven historically Black colleges and universities (HBCUs) across the United States received back-to-back bomb threats this week, forcing students to evacuate or shelter in place while authorities investigated. The threats come amid a dramatic rise in bombings in the US and follow bomb threats at other US colleges last November." , 
		"Pfizer and BioNTech have begun a clinical trial for their Omicron-specific Covid-19 vaccine candidate, they announced in a news release on Tuesday. The study will evaluate the vaccine for safety, tolerability and the level of immune response, as both a primary series and a booster dose, in up to 1420 healthy adults ages 18 to 55." , 
		"The number of people already infected by the mystery virus emerging in China is far greater than official figures suggest, scientists have told the BBC. There have been more than 60 confirmed cases of the new coronavirus, but UK experts estimate a figure nearer 1700. Two people are known to have died from the respiratory illness, which appeared in Wuhan city in December." , 
		"The World Health Organization on Wednesday declared the novel coronavirus outbreak a pandemic. There are 118000 cases, more than 4000 deaths, the agency said, and the virus has found a foothold on every continent except for Antarctica." , 
		"With the justices sheltering at home, the Supreme Court had been shut down to live arguments until this past October. The court remains closed to the public, and lawyers arguing in the court have to be masked and provide proof of a negative Covid test. Omicron is still ravaging America, and the military has been dispatched to help overwhelmed hospitals. Yet on Thursday the Supreme Court conservative majority struck down the temporary vaccine mandate for large businesses proposed by the Occupational Safety and Health Administration and sided with Covid19, thereby guaranteeing that the pandemic will continue into a third year of misery for Americans." ,
		"A firefighter and his crew battled to keep the raging Glass Fire from devastating an upmarket Napa Valley vineyard. The firefighter denies lighting backfires which consume fuel in a wildfire's path but admits his team failed to advise Cal Fire, the state's fire agency that it was in the evacuated area, as required by law." , 
		"The incident highlights how a booming business in private firefighting is creating friction with government firefighters as wildfires grow more frequent and dangerous across the western US. It also underscores the inequity of who receives protection. Businesses and wealthy property owners have growing options to protect themselves, for a price. Meanwhile, homeowners across California are being denied homeowner's insurance renewals because of wildfire risk." ,
	]
}

function fillExampleSelectField() {
	hideResult();
	lang="eng";
	// alert("examples...");
	$("#example").empty();
	selectField = document.getElementById("example");
	textField = document.getElementById("text");
	idx = 0;
	for (var example in xel_examples[lang]) {
		var opt = document.createElement("option");
		opt.value=idx;
		opt.innerHTML = xel_examples[lang][idx].substring(0,50)+"..."; 
		selectField.appendChild(opt);
		idx += 1;
	}	
	selectField.value = "0";
	textField.value = xel_examples[lang][0];
}

function newExampleSelect() {
	hideResult();
	// langSelectField = document.getElementById("lang");
	lang = "eng"; // langSelectField.value;
	exampleSelectField = document.getElementById("example");
	example = exampleSelectField.value;
	textField = document.getElementById("text");
	// textField.value = xel_langs[languageSelected]["text"]; 
	textField.value = xel_examples[lang][example]; 
}

function getSelectedAnnotators() {
	var selectedAnnotators = [];
	var annotator_buttons = document.getElementsByClassName('annotator');
	for(var i = 0; i<annotator_buttons.length;i++)
	{
		var ann_button = annotator_buttons[i];
		//console.log(checkbox_button);
		if(ann_button.checked) {
			//alert(ann_button.id);
			var text_of_button = ann_button.id;
			//console.log(text_of_button);
			selectedAnnotators.push(text_of_button);
		}
	}
	return selectedAnnotators;
}

function hideResult() {
	$("#result").hide();
	$("#result").html("");
}

function showResult() {
	$("#result").show();
}

/*
async function httpPOST(url = '', data = {}, pfunction) {
  console.log(url);
  console.log(JSON.stringify(data));
  fetch(url, {
    method: 'POST',
    mode: 'no-cors',
	cache: 'no-cache',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }).then(resp => resp.json())
        .then(json => {
                pfunction(json);
        });
}
*/

async function postInput(url = '', data = {}) {
	const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    //mode: 'no-cors', // no-cors, *cors, same-origin
    // cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    // credentials: 'omit', // include, *same-origin, omit
    headers: {
        'Content-Type': 'application/json',
       // 'Accept': 'application/json, text/plaini, */*'
      //'Content-Type': 'application/json'
        //,'Data-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    // redirect: 'follow', // manual, *follow, error
    // referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data) // body data type must match "Content-Type" header
    //body: data
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

function formSubmit() {
	hideResult();
	$("#result").html("Working...");
	showResult();
	anns = getSelectedAnnotators();
	text = document.getElementById("text").value;
	data = {
		"text": text,
		"anns": anns
	};
	url = "view";
	postInput(url, data)
		.then(data => {
			// console.log(data);
			$("#result").html(data.html);
			showResult();
    });
	// $("#result").html(anns.join(","));
	// showResult();
	return false;
}

function main() {
	fillExampleSelectField();
}


