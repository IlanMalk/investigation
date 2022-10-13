fileName='AdamDriver_2015P.sph';
[a,b,c,d]=v_readsph(fileName);
%newWav=v_writewav(a,b,'new');
%plot(a);

[e,f]=v_melcepst(a,b);

plot(f,e)

