$( document ).ready(function() {
  getDataForDatatables();
});

function getDataForDatatables(){

var url = window.location.href;
var org_id = decodeURIComponent(url.split("?").pop());
var org_name = org_id.split('|')[0].trim();
$('h2').html('List of <i>"http"</i> and <i>"ftp"</i> urls: ' + org_name)

$.getJSON( "orgs_http_data.json", function( data ) {
setDataToTable(data[org_id]);
});
}

function setDataToTable(jsonData){
$('#employee').DataTable( {
  "autoWidth": false,
pagination: "bootstrap",
  filter:true,
  data: jsonData,
  destroy: true,
  pageLength: 25,
  "columns":[  
    {"data": "dataset"},
    {"data": "url"},
    {"data": "url_type"},
    {"data": "dataset_id"},
    {"data": "id"},
  ],
  columnDefs: [
  { "width": "25%", "targets": 0 },
  { "width": "40%", "targets": 1 },
        {
        targets: 3,
        render: function (data, type, row, meta)
        {

            data = '<a target="_blank" href="https://open.canada.ca/data/en/dataset/' + data + '">View dataset</a>';
            return data;
        }
        },
        {
        targets: 4,
        render: function (data, type, row, meta)
        {
            data = '<a target="_blank" href="https://registry.open.canada.ca/en/dataset/' + row.dataset_id + '/resource_edit/' + data + '">Edit resource</a>';
            return data;
        }
        }],
} );
}