//服务层
app.service('brandService',function($http){
	var URL = "http://localhost:8989/shopping-manager/";
	
	//读取列表数据绑定到表单中
	this.findAll=function(){
		return $http.get(URL+'brand-Ms/findAll');		
	}
	//分页 
	this.findPage=function(page,rows){
		return $http.get(URL+'brand-Ms/findPage?page='+page+'&rows='+rows);
	}
	//查询实体
	this.findOne=function(id){
		return $http.get(URL+'brand-Ms/findBrandDetail?id='+id);
	}
	//增加 
	this.add=function(entity){
		return  $http.post(URL+'brand-Ms/add',entity );
	}
	//修改 
	this.update=function(entity){
		return  $http.post(URL+'brand-Ms/updateBrand',entity );
	}
	//删除
	this.dele=function(ids){
		return $http.get(URL|+'brand-Ms/delete?ids='+ids);
	}
	//搜索
	this.search=function(page,rows,searchEntity){
		return $http.post(URL+'../brand/search.do?page='+page+"&rows="+rows, searchEntity);
	}    
	//下拉列表数据
	this.selectOptionList=function(){
		return $http.get(URL+'brand-Ms/selectOptionList');
	}
	
});
