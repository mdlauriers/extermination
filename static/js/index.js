document.addEventListener('DOMContentLoaded', function () {
    var options = {
        "format": "yyyy-mm-dd",
        "i18n": {
            cancel: "Annuler",
            clear: "Effacer",
            done: "Sélectionner",
            months: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août",
                "Septembre", "Octobre", "Novembre", "Décembre"
            ],
            monthsShort: ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov",
                "Dec"
            ],
            weekdays: ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
            weekdaysShort: ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"],
            weekdaysAbbrev: ["D", "L", "M", "M", "J", "V", "S"]
        },
        "maxDate": new Date()
    }
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems, options);
});

$("#search_from_date").on('click', function () {
    $("#search_to_date").removeAttr("disabled");
});

$("#quick_search_declarations_button").on("click", function () {
    // Supprimer les messages d'erreur.
    $(".error-message").addClass("hide");

    // Obtenir les dates de début et de fin.
    var date_debut = document.getElementById("search_from_date");
    date_debut = M.Datepicker.getInstance(date_debut);
    date_debut = date_debut.toString();

    var date_fin = document.getElementById("search_to_date");
    date_fin = M.Datepicker.getInstance(date_fin);
    date_fin = date_fin.toString();


    // Si la date de début est supérieure à la date de fin, on ne procède pas.
    if (date_debut >= date_fin) {
        console.log("erreur");
        $(".error-message").removeClass("hide");
    } else {
        $("#quick_search_form").hide("slide", { direction: "left" }, 1000, () => {
            $("#quick_search_results").fadeIn(500);
        });
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Transformer les donnees en objet JSON.
                    var declarations = JSON.parse(xhr.response);
                    var arrondissements = [];
                    var quartiers = [];
                    var nb_declarations = [];

                    for (var i in declarations) {
                        if (!quartiers.includes(declarations[i].nom_qr)) {
                            quartiers.push(declarations[i].nom_qr);
                            arrondissements.push(declarations[i].nom_arrond);
                            nb_declarations.push(1);
                        } else {
                            var index = quartiers.indexOf(declarations[i].nom_qr);
                            nb_declarations[index] = nb_declarations[index] + 1;
                            arrondissements.push(declarations[i].nom_arrond);
                        }
                    }
                    for (var i in quartiers) {
                        $("#quick_research_results_table").find('tbody').append('<tr><td>' + arrondissements[i] + '</td><td>' + quartiers[i] + '</td><td>' + nb_declarations[i] + '</td></tr>');
                    }
                    var quartier = $("#quartiers").val()
                    enable_table(quartier);
                } else {
                    console.log('Erreur avec le serveur lors de la requete.');
                }
            }
        }
        xhr.open("GET", "/declarations?du=" + date_debut + "&au=" + date_fin);
        xhr.send();
    }
});

function enable_table(quartier) {
    
    if(quartier != null){
        data = {
            "language": {
                url: 'http://cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
            },
            "bFilter": true,
            "scrollY": "500px",
            "scrollX": false,
            "scrollCollapse": true,
            "paging": false,
            "order": [
                [0, "asc"]
            ],
            "oSearch": {"sSearch": quartier}
        }
    } else {
        data = {
            "language": {
                url: 'http://cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
            },
            "bFilter": true,
            "scrollY": "500px",
            "scrollX": false,
            "scrollCollapse": true,
            "paging": false,
            "order": [
                [0, "asc"]
            ]
        }
    }
    $('#quick_research_results_table').DataTable(data);
}