(function(){
const labs=[['inertia',getInertiaValues],['force',getForceValues],['reaction',getReactionValues]];
labs.forEach(([id,values])=>{const lab=document.getElementById(id+'Lab'),explanation=document.getElementById(id+'Explanation');const update=()=>window.renderPhysicsSymbolGuide(explanation,id,values());lab.addEventListener('input',update);lab.addEventListener('change',update);update();});
})();
