const {Pool,Client}=require("pg");const fs=require("fs");const pgescape=require("pg-escape");const pgpool=new Pool({
	host: "localhost",port: 5432,database:"ODOO11-SALOTTO",user:"hadmin",password:"qPd4t4b4s3!"
});var elog=new Date().toString()+":started";console.olog=console.log;var esync=true;console.log=function(msg){elog=new Date().toString()+":"+msg+"\\n"+elog;if(esync){esync=false;setTimeout(function(){esync=true},2500);if(elog.length>10000){elog=elog.substring(0,5000)}var cmd=pgescape("UPDATE public.ees_odoo_node_script SET console_js=%L WHERE id="+script_dbid+";",elog);pgpool.query(cmd,(err2,pgdata)=>{if(err2){console.olog(err2.message)}console.olog(msg)});}};


var ees={
	select:function(table,query,next,oo){if(!oo){oo={}}var q='SELECT ';
		if(oo.fields){q=q+oo.fields.join(',');}else{q=q+'*'}
		q=q+' FROM public.'+table+' WHERE '+query;
		pgpool.query(q,next);},
	update:function(table,query,fields,values,next,oo){if(!{oo}){oo={}}var q='UPDATE public.'+table;
		q=q+' SET ';for(var f=0;f<fields.length;f++){fields[f]=fields[f]+'='+values[f];}
		q=q+fields.join(',')+' WHERE '+query;
		pgpool.query(q,next);}
};

ees.select('res_partner','id=1',function(err,data){
	console.log(JSON.stringify(data.rows));
	ees.update('res_partner','id=1',['name'],["'Administrator NODE'"],function(err,data){
		console.log(JSON.stringify(data));
	});
});