function submitForm(name){
    let last = document.getElementById("last-selected");
    last.value = name;
    document.getElementById("artist-picker").submit();
}

function deselect(){
    var fldSet = document.getElementById("cboxfield");
    var chkBoxes = fldSet.getElementsByTagName('input'); 
    for(var i=0;i<chkBoxes.length;i++){ 
        if(chkBoxes[i].type == 'checkbox'){
            chkBoxes[i].checked = false;
        }
    }
}

function hideshow(){
    var cbox = document.getElementById("cboxfield");
    cbox.hidden = !cbox.hidden;

    var button = document.getElementById("hider");
    if (button.value == "Hide Artists"){
        button.value = "Show Artists";
    }else{
        button.value = "Hide Artists";
    }
}

/* Credit Calumah from StackOverflow */
function download_table_as_csv(table_id, separator = ',') {
    // Select rows from table_id
    var rows = document.querySelectorAll('table#' + table_id + ' tr');
    // Construct csv
    var csv = [];
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll('td, th');
        for (var j = 0; j < cols.length; j++) {
            // Clean innertext to remove multiple spaces and jumpline (break csv)
            var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
            // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
            data = data.replace(/"/g, '""');
            // Push escaped string
            row.push('"' + data + '"');
        }
        csv.push(row.join(separator));
    }
    var csv_string = csv.join('\n');
    // Download it
    var filename = 'RIJF2024.csv';
    var link = document.createElement('a');
    link.style.display = 'none';
    link.setAttribute('target', '_blank');
    link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
