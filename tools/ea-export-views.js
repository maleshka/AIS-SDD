!INC Local Scripts.EAConstants-JScript

/*
 * Export views pre SDD (R-002) zo Sparx EA do spec/architecture/views/.
 * Spustenie: v otvorenom modeli Specialize > Scripting (alebo Ctrl+Alt+... podľa verzie) >
 * nový JScript v ľubovoľnej skupine > vložiť tento text > Run.
 * Ak riadok !INC hlási chybu, zmažte ho – skript ho nepotrebuje.
 */

var OUT = "Z:\\Users\\maleshka\\STU\\1.rocnik_I\\AIS\\SDD-Ticket\\spec\\architecture\\views\\";

var MAP = {
  "Motivation Viewpoint": "B-01-motivation.jpg",
  "solution concept TO BE": "B-01-solution-concept-to-be.jpg",
  "Layered Viewpoint TO BE": "B-01-layered-to-be.jpg",
  "Business Process Cooperation Viewpoint TO BE": "B-01-business-process-cooperation-to-be.jpg",
  "Service realization viewpoint": "B-01-service-realization.jpg",
  "Application usage viewpoint TO BE": "B-01-application-usage-to-be.jpg",
  "Application structure viewpoint TO BE": "B-01-application-structure-to-be.jpg",
  "Application cooperation viewpoint TO BE": "B-01-application-cooperation-to-be.jpg",
  "Information structure viewpoint": "B-01-information-structure.jpg",
  "Technology Usage Viewpoint TO BE": "B-01-technology-usage-to-be.jpg",
  "Technology Viewpoint TO BE": "B-01-technology-to-be.jpg",
  "Implementation and Migration Viewpoint": "B-01-implementation-migration.jpg",
  "Enterprise Continuum": "B-01-enterprise-continuum.jpg",
  "Gap Analysis": "B-01-gap-analysis.jpg"
};

var pi = Repository.GetProjectInterface();
var count = 0;

function walk(pkg) {
  for (var i = 0; i < pkg.Diagrams.Count; i++) {
    var d = pkg.Diagrams.GetAt(i);
    var file = MAP[d.Name];
    if (file) {
      var ok = pi.PutDiagramImageToFile(pi.GUIDtoXML(d.DiagramGUID), OUT + file, 1);
      Session.Output((ok ? "OK    " : "CHYBA ") + d.Name + "  ->  " + file);
      count++;
    }
  }
  for (var j = 0; j < pkg.Packages.Count; j++) {
    walk(pkg.Packages.GetAt(j));
  }
}

Session.Output("Export views pre SDD – začiatok");
for (var m = 0; m < Repository.Models.Count; m++) {
  walk(Repository.Models.GetAt(m));
}
Session.Output("Hotovo: " + count + " z 14 diagramov.");
