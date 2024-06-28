package com.online.shopping.service.impl;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.github.pagehelper.Page;
import com.github.pagehelper.PageHelper;
import com.online.shopping.entity.PageResult;
import com.online.shopping.mapper.TbBrandMapper;
import com.online.shopping.pojo.TbBrand;
import com.online.shopping.service.BrandService;

@Service
public class BrandServiceImpl implements BrandService {
	
	@Autowired
	private TbBrandMapper brandMapper;
	
	@Override
	public List<TbBrand> findAll() {
		return brandMapper.selectByExample(null);
	}

	@Override
	public PageResult findPage(int pageNum, int pageSize) {
		PageHelper.startPage(pageNum, pageSize);
		Page<TbBrand> page = (Page<TbBrand>) brandMapper.selectByExample(null);
		return new PageResult(page.getTotal(), page.getResult());
	}

	@Override
	public void add(TbBrand brand) {
		brandMapper.insert(brand);
	}

	@Override
	public TbBrand findOne(Long id) {
		return brandMapper.selectByPrimaryKey(id);
	}

	@Override
	public void update(TbBrand brand) {
		brandMapper.updateByPrimaryKey(brand);
	}

	@Override
	public void delete(Long[] ids) {
		for (Long id : ids) {
			brandMapper.deleteByPrimaryKey(id);
		}
		
	}

	/**
	 * 
	 * {"id":1,"text":"联想"},{"id":2,"text":"华为"},{"id":3,"text":"三星"},{"id":4,"text":"小米"},{"id":5,"text":"OPPO"},{"id":6,"text":"360"},{"id":7,"text":"中兴"},{"id":8,"text":"魅族"},{"id":9,"text":"苹果"},{"id":10,"text":"VIVO"},{"id":11,"text":"诺基亚"},{"id":12,"text":"锤子"},{"id":13,"text":"长虹"},{"id":14,"text":"海尔"},{"id":15,"text":"飞利浦"},{"id":16,"text":"TCL"},{"id":17,"text":"海信"},{"id":18,"text":"夏普"},{"id":19,"text":"创维"},{"id":20,"text":"东芝"},{"id":21,"text":"康佳"},{"id":26,"text":"华帝"},{"id":27,"text":"金龙鱼"}]
	 * 
	 */
	@Override
	public List<Map> selectOptionList() {
		return brandMapper.selectOptionList();
	}

}
