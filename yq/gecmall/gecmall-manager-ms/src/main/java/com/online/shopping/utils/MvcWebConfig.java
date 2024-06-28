package com.online.shopping.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

@Configuration
public class MvcWebConfig extends WebMvcConfigurerAdapter {

	
	@Autowired
	private FileUploadProperteis fileUploadProperteis;

//	@Override
//	public void addResourceHandlers(ResourceHandlerRegistry registry) {
//		//addResourceHandler表示映射路径 
//		//addResourceLocations表示物理路径 
//		registry.addResourceHandler("/upload/**").addResourceLocations("file:D:/file/");
//	}
	
	@Override
	public void addResourceHandlers(ResourceHandlerRegistry registry) {
		
		registry.addResourceHandler(fileUploadProperteis.getStaticAccessPath()).addResourceLocations("file:"+fileUploadProperteis.getUploadFolder()+"/");
	}
	
}
