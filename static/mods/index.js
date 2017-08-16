﻿/**

 @Name: Fly社区主入口

 */
 

layui.define(['layer','laypage','laytpl', 'form', 'upload', 'util'], function(exports){

  var $ = layui.jquery
  ,layer = layui.layer
  ,laytpl = layui.laytpl
  ,form = layui.form()
  //,util = layui.util
  ,laypage=layui.laypage
  ,device = layui.device();
  
  //阻止IE7以下访问
  if(device.ie && device.ie < 8){
    layer.alert('如果您非得使用ie浏览Fly社区，那么请使用ie8+');
  }
  
  layui.focusInsert = function(obj, str){
    var result, val = obj.value;
    obj.focus();
    if(document.selection){ //ie
      result = document.selection.createRange(); 
      document.selection.empty(); 
      result.text = str; 
    } else {
      result = [val.substring(0, obj.selectionStart), str, val.substr(obj.selectionEnd)];
      obj.focus();
      obj.value = result.join('');
    }
  };
  
  var gather = {
     
    //Ajax
    json: function(url, data, success, options){
      var that = this;
      options = options || {};
      data = data || {};
      console.log(url);
      return $.ajax({
        type: options.type || 'post',
        dataType: options.dataType || 'json',
        headers: {'Content-Type': 'application/json',"X-CSRFToken":csrftoken},
        data: data,
        url: url,
        success: function(res){
          if(res.status === 0) {
            success && success(res);
          } else {
            layer.msg(res.msg||res.code, {shift: 6});
          }
        }, error: function(xhr,err){
          options.error || layer.msg('请求异常，请重试hahahahah', {shift: 6});
        }
      });
    },
    jsonn: function(url, data, success, options){
      var that = this;
      options = options || {};
      data = data || {};
      return $.ajax({
        type: options.type || 'post',
        dataType: options.dataType || 'json',
        //headers: {'Content-Type': 'application/json',"X-CSRFToken":csrftoken},
        data: data,
        url: url,
        success: function(res){
          if(res.status === 0) {
            success && success(res);
          } else {
            layer.msg(res.msg||res.code, {shift: 6});
          }
        }, error: function(xhr,err){
          console.log(xhr);
          options.error || layer.msg('请求异常，请重试hahahahah', {shift: 6});
        }
      });
    }
     //多久前
    ,time: function(time, brief){
      var stamp = new Date().getTime() - time;
      if(stamp > 1000*60*60*24*30){
        stamp =  new Date(time).toLocaleString('chinese', {
          hour12: false
        }).replace(/\//g, '-');
        brief && (stamp = stamp.replace(/\s[\S]+$/g, ''));
        return stamp;
      }
      if(stamp >= 1000*60*60*24){
        return ((stamp/1000/60/60/24)|0) + '天前';
      } else if(stamp >= 1000*60*60){
        return ((stamp/1000/60/60)|0) + '小时前';
      } else if(stamp >= 1000*60*5){
        return ((stamp/1000/60)|0) + '分钟前';
      } else {
        return '刚刚';
      }
    }
    //将普通对象按某个key排序
    ,sort: function(data, key, asc){
      var obj = JSON.parse(JSON.stringify(data));
      var compare = function (obj1, obj2) { 
        var value1 = obj1[key]; 
        var value2 = obj2[key]; 
        if (value2 < value1) { 
          return -1; 
        } else if (value2 > value1) { 
          return 1; 
        } else { 
          return 0; 
        } 
      };
      obj.sort(compare);
      if(asc) obj.reverse();
      return obj;
    }

    //计算字符长度
    ,charLen: function(val){
      var arr = val.split(''), len = 0;
      for(var i = 0; i <  val.length ; i++){
        arr[i].charCodeAt(0) < 299 ? len++ : len += 2;
      }
      return len;
    }
    
    ,form: {}

    //简易编辑器
    ,layEditor: function(options){
      var html = '<div class="fly-edit">'
        +'<span type="face" title="插入表情"><i class="iconfont icon-biaoqing"></i>表情</span>'
        +'<span type="picture" title="插入图片：img[src]"><i class="iconfont icon-tupian"></i>图片</span>'
        +'<span type="href" title="超链接格式：a(href)[text]"><i class="iconfont icon-lianjie"></i>链接</span>'
        +'<span type="code" title="插入代码"><i class="iconfont icon-daima"></i>代码</span>'
        +'<span type="yulan" title="预览"><i class="iconfont icon-yulan"></i>预览</span>'
      +'</div>';
      var log = {}, mod = {
        picture: function(editor){ //插入图片
          layer.open({
            type: 1
            ,id: 'fly-jie-upload'
            ,title: '插入图片'
            ,area: 'auto'
            ,shade: false
            ,area: '465px'
            ,skin: 'layui-layer-border'
            ,content: ['<ul class="layui-form layui-form-pane" style="margin: 20px;">'
              ,'<li class="layui-form-item">'
                ,'<label class="layui-form-label">URL</label>'
                ,'<div class="layui-input-inline">'
                    ,'<input required name="image" placeholder="支持直接粘贴远程图片地址" value="" class="layui-input">'
                  ,'</div>'
                  ,'<input required type="file" name="file" class="layui-upload-file" value="">'
              ,'</li>'
              ,'<li class="layui-form-item" style="text-align: center;">'
                ,'<button type="button" lay-submit lay-filter="uploadImages" class="layui-btn">确认</button>'
              ,'</li>'
            ,'</ul>'].join('')
            ,success: function(layero, index){
              var image =  layero.find('input[name="image"]');
              layui.upload({
                url: '/api/upload/'
                ,elem: '#fly-jie-upload .layui-upload-file'
                ,success: function(res){
                  if(res.status === 0){
                    image.val(res.url);
                  } else {
                    layer.msg(res.msg, {icon: 5});
                  }
                }
              });
              
              form.on('submit(uploadImages)', function(data){
                var field = data.field;
                if(!field.image) return image.focus();
                layui.focusInsert(editor[0], 'img['+ field.image + '] ');
                layer.close(index);
              });
            }
          });
        }
        ,face: function(editor, self){ //插入表情
          var str = '', ul, face = gather.faces;
          for(var key in face){
            str += '<li title="'+ key +'"><img src="'+ face[key] +'"></li>';
          }
          str = '<ul id="LAY-editface" class="layui-clear">'+ str +'</ul>';
          layer.tips(str, self, {
            tips: 3
            ,time: 0
            ,skin: 'layui-edit-face'
          });
          $(document).on('click', function(){
            layer.closeAll('tips');
          });
          $('#LAY-editface li').on('click', function(){
            var title = $(this).attr('title') + ' ';
            layui.focusInsert(editor[0], 'face' + title);
          });
        }
        ,href: function(editor){ //超链接
          layer.prompt({
            title: '请输入合法链接'
            ,shade: false
          }, function(val, index, elem){
            if(!/^http(s*):\/\/[\S]/.test(val)){
              layer.tips('这根本不是个链接，不要骗我。', elem, {tips:1})
              return;
            }
            layui.focusInsert(editor[0], ' a('+ val +')['+ val + '] ');
            layer.close(index);
          });
        }
        ,code: function(editor){ //插入代码
          layer.prompt({
            title: '请贴入代码'
            ,formType: 2
            ,maxlength: 10000
            ,shade: false
            ,area: ['830px', '390px']
          }, function(val, index, elem){
            layui.focusInsert(editor[0], '[pre]\n'+ val + '\n[/pre]');
            layer.close(index);
          });
        }
        ,yulan: function(editor){ //预览
          var content = editor.val();
          
          content = /^\{html\}/.test(content) 
            ? content.replace(/^\{html\}/, '')
          : gather.content(content);

          layer.open({
            type: 1
            ,title: '预览'
            ,area: ['60%', '60%']
            ,scrollbar: false
            ,content: '<div class="detail-body" style="margin:20px;">'+ content +'</div>'
          });
        }
      };
      
      layui.use('face', function(face){
        options = options || {};
        gather.faces = face;
        $(options.elem).each(function(index){
          var that = this, othis = $(that), parent = othis.parent();
          parent.prepend(html);
          parent.find('.fly-edit span').on('click', function(event){
            var type = $(this).attr('type');
            mod[type].call(that, othis, this);
            if(type === 'face'){
              event.stopPropagation()
            }
          });
        });
      });
      
    }

    ,escape: function(html){
      return String(html||'')
          .replace(/&(?!#?[a-zA-Z0-9]+;)/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, '&#39;').replace(/"/g, '&quot;');
    }

    //内容转义
    ,content: function(content){
      //支持的html标签
      var html = function(end){
        return new RegExp('\\['+ (end||'') +'(pre|div|table|thead|th|tbody|tr|td|ul|li|ol|li|dl|dt|dd|h2|h3|h4|h5)\\]\\n*', 'g');
      };
      content = gather.escape(content||'') //XSS
      .replace(/img\[([^\s]+?)\]/g, function(img){  //转义图片
        return '<img src="/' + img.replace(/(^img\[)|(\]$)/g, '') + '">';
      }).replace(/@(\S+)(\s+?|$)/g, '@<a href="javascript:;" class="fly-aite">$1</a>$2') //转义@
      .replace(/face\[([^\s\[\]]+?)\]/g, function(face){  //转义表情
        var alt = face.replace(/^face/g, '');
        return '<img alt="'+ alt +'" title="'+ alt +'" src="' + gather.faces[alt] + '">';
      }).replace(/a\([\s\S]+?\)\[[\s\S]*?\]/g, function(str){ //转义链接
        var href = (str.match(/a\(([\s\S]+?)\)\[/)||[])[1];
        var text = (str.match(/\)\[([\s\S]*?)\]/)||[])[1];
        if(!href) return str;
        var rel =  /^(http(s)*:\/\/)\b(?!(\w+\.)*(sentsin.com|layui.com))\b/.test(href.replace(/\s/g, ''));
        return '<a href="'+ href +'" target="_blank"'+ (rel ? ' rel="nofollow"' : '') +'>'+ (text||href) +'</a>';
      }).replace(html(), '\<$1\>').replace(html('/'), '\</$1\>') //转移代码
      .replace(/\n/g, '<br>') //转义换行   
      return content;
    }
    
    //新消息通知
    ,newmsg: function(){
      if(layui.cache.user.uid !== -1){
        gather.json('/message/nums/', {
          _: new Date().getTime()
        }, function(res){
          if(res.status === 0 && res.count > 0){
            var msg = $('<a class="nav-message" href="javascript:;" title="您有'+ res.count +'条未阅读的消息">'+ res.count +'</a>');
            $('.nav-user').append(msg);
            msg.on('click', function(){
              gather.json('/message/read', {}, function(res){
                if(res.status === 0){
                  location.href = '/user/message/';
                }
              });
            });
          }
        });
      }
      return arguments.callee;
    }

    ,cookie: function(e,o,t){
      e=e||"";var n,i,r,a,c,p,s,d,u;if("undefined"==typeof o){if(p=null,document.cookie&&""!=document.cookie)for(s=document.cookie.split(";"),d=0;d<s.length;d++)if(u=$.trim(s[d]),u.substring(0,e.length+1)==e+"="){p=decodeURIComponent(u.substring(e.length+1));break}return p}t=t||{},null===o&&(o="",t.expires=-1),n="",t.expires&&("number"==typeof t.expires||t.expires.toUTCString)&&("number"==typeof t.expires?(i=new Date,i.setTime(i.getTime()+864e5*t.expires)):i=t.expires,n="; expires="+i.toUTCString()),r=t.path?"; path="+t.path:"",a=t.domain?"; domain="+t.domain:"",c=t.secure?"; secure":"",document.cookie=[e,"=",encodeURIComponent(o),n,r,a,c].join("");
    }
 //插入右下角悬浮bar
    ,rbar: function(){
      var style = $('head').find('.fly-style'), skin = {
        stretch: 'charushuipingxian'
      };

      var html = $('<ul class="fly-rbar">'
        +'<li class="iconfont icon-'+ (skin[gather.cookie('fly-style')]||'huizongzuoyoutuodong') +'" method="'+ (gather.cookie('fly-style') === 'stretch' ? 'reset' : 'stretch') +'"></li>'
        +'<li id="F_topbar" class="iconfont icon-top" method="top"></li>'
      +'</ul>');
      var dict = {
        stretch: function(othis){
          style.attr('href', style.data('href'));
          othis.attr({
            method: 'reset'
            ,'class': 'iconfont icon-charushuipingxian'
          });
          gather.cookie('fly-style', 'stretch', {
            path: '/'
            ,expires: 365
          });
        }
        ,reset: function(othis){
          style.removeAttr('href');
          othis.attr({
            method: 'stretch'
            ,'class': 'iconfont icon-huizongzuoyoutuodong'
          });
          gather.cookie('fly-style','reset', {
            path: '/'
          });
        }
        ,top: function(othis){
          $('html,body').animate({scrollTop: 0}, 100, function(){
            othis.hide();
          });
        }
      };
      //gather.cookie('fly-style')==='stretch'?style.attr('href', style.data('href')):style.removeAttr('href');

      //dict[gather.cookie('fly-style')].call(this, $(this));
      $('body').append(html);

      //事件
      html.find('li').on('click', function(){
        var othis = $(this), method = othis.attr('method');
        dict[method].call(this, othis);
      });

      //滚动
      var log = 0, topbar = $('#F_topbar'), scroll = function(){
        var stop = $(window).scrollTop();
        if(stop >= 200){
          if(!log){
            topbar.show();
            log = 1;
          }
        } else {
          if(log){
            topbar.hide();
            log = 0;
          }
        }
        return arguments.callee;
      }();
      $(window).on('scroll', scroll);
    }
  };

  //相册
  /*layer.photos({
    photos: '.photos'
    ,zIndex: 9999999999
    ,anim: -1
  });*/




  //搜索
  $('.fly-search').submit(function(){
    var input = $(this).find('input'), val = input.val();
    if(val.replace(/\s/g, '') === ''){
      return false;
    }
    input.val('site:layui.com '+ input.val());
  });
  $('.icon-sousuo').on('click', function(){
    $('.fly-search').submit();
  });
  //搜索
    /*
  $('.fly-search').on('click', function(){
    layer.open({
      type: 1
      ,title: false
      ,closeBtn: false
      //,shade: [0.1, '#fff']
      ,shadeClose: true
      ,maxWidth: 10000
      ,skin: 'fly-layer-search'
      ,content: ['<form action="http://cn.bing.com/search">'
        ,'<input autocomplete="off" placeholder="搜索内容，回车跳转" type="text" name="q">'
      ,'</form>'].join('')
      ,success: function(layero){
        var input = layero.find('input');
        input.focus();

        layero.find('form').submit(function(){
          var val = input.val();
          if(val.replace(/\s/g, '') === ''){
            return false;
          }
          input.val('site:layui.com '+ input.val());
      });
      }
    })
  });
*/
  //新消息通知
  gather.newmsg();

  //发送激活邮件
  gather.activate = function(email){
    gather.json('/api/activate/', {}, function(res){
      if(res.status === 0){
        layer.alert('已成功将激活链接发送到了您的邮箱，接受可能会稍有延迟，请注意查收。', {
          icon: 1
        });
      };
    });
  };
  $('#LAY-activate').on('click', function(){
    gather.activate($(this).attr('email'));
  });

  //点击@
  $('body').on('click', '.fly-aite', function(){
    var othis = $(this), text = othis.text();
    if(othis.attr('href') !== 'javascript:;'){
      return;
    }
    text = text.replace(/^@|（[\s\S]+?）/g, '');
    othis.attr({
      href: '/jump?username='+ text
      ,target: '_blank'
    });
  });

  //表单提交
  form.on('submit(*)', function(data){
    var action = $(data.form).attr('action'), button = $(data.elem);
    gather.json(action, data.field, function(res){
      var end = function(){
        if(res.action){
          location.href = res.action;
        } else {
          gather.form[action||button.attr('key')](data.field, data.form);
        }
      };
      if(res.status === 0){
        button.attr('alert') ? layer.alert(res.msg, {
          icon: 1,
          time: 10*1000,
          end: end
        }) : end();
      }
    });
    return false;
  });
  /*
  //文章表单提交
  form.on('submit(ar)', function(data){
    var action = $(data.form).attr('action'), button = $(data.elem);
    data.field.content=gather.content(data.field.content);
      $('#L_content').val(data.field.content);
    gather.json(action, data.field, function(res){
      var end = function(){
        if(res.action){
          location.href = res.action;
        } else {
          gather.form[action||button.attr('key')](data.field, data.form);
        }
      };
      if(res.status === 0){
        button.attr('alert') ? layer.alert(res.msg, {
          icon: 1,
          time: 10*1000,
          end: end
        }) : end();
      };
    });
    return false;
  });
  */
  //加载特定模块
  if(layui.cache.page && layui.cache.page !== 'index'){
    var extend = {};
    extend[layui.cache.page] = layui.cache.page;
    layui.extend(extend);
    layui.use(layui.cache.page);
  }
  
  //加载IM
  if(!device.android && !device.ios){
    //layui.use('im');
  }

  //加载编辑器
  gather.layEditor({
    elem: '.fly-editor'
  });

  //右下角固定Bar
  gather.rbar();


  //手机设备的简单适配
  var treeMobile = $('.site-tree-mobile')
  ,shadeMobile = $('.site-mobile-shade')

  treeMobile.on('click', function(){
    $('body').addClass('site-mobile');
  });

  shadeMobile.on('click', function(){
    $('body').removeClass('site-mobile');
  });

  //图片懒加载
  /*
  layui.use('flow', function(flow){
    flow.lazyimg();
  });*/
  //分页



  exports('fly', gather);

});

