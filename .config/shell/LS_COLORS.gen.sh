#!/usr/bin/env bash
for i in {'alacritty*','screen*','tmux*','xterm*'}; do
	echo 'TERM '$i
done

for i in {NORMAL,FILE,RESET,MISSING}; do
	echo "$i 0"
done

echo 'DIR 01;34' # directory
echo 'LINK 01;36' # symbolic link
echo 'MULTIHARDLINK 01' # regular file with more than one link
echo 'FIFO 40;33' # pipe
echo 'SOCK 01;35' # socket
echo 'BLK 40;33;01' # block device driver
echo 'CHR 40;33;01' # character device driver
echo 'ORPHAN 40;31;01' # symlink to nonexistent file, or non-stat'able file ...
echo 'SETUID 37;41' # file that is setuid (u+s)
echo 'SETGID 30;43' # file that is setgid (g+s)
echo 'CAPABILITY 30;41' # file with capability, getcap <file>
echo 'STICKY_OTHER_WRITABLE 30;42' # dir that is sticky and other-writable (+t,o+w)
echo 'OTHER_WRITABLE 34;42' # dir that is other-writable (o+w) and not sticky
echo 'STICKY 37;44' # dir with the sticky bit set (+t) and not other-writable
echo 'EXEC 01;32' # excute perm

# archives or compressed files
for i in {gz,tar,tgz,lzma,zip,z,xz,zst,bz2,deb,rpm,jar,rar,cpio,7z,cab}; do
	echo ".$i 01;31"
done

# images
for i in {jpg,jpeg,gif,bmp,tga,tif,tiff,png,svg}; do
	echo ".$i 00;35"
done

# videos
for i in {mpg,mpeg,webm,ogm,mp4,mp4v,vob,wmv,asf,rmvb,avi,flv,mkv}; do
	echo ".$i 01;35"
done

# audios
for i in {aac,au,flac,m4a,mid,midi,mp3,ogg,wav,opus}; do
	echo ".$i 00;36"
done

# binary documents
for i in {doc,docx,xlsx,xls,pdf,pptx,ppt,ods,odt}; do
	echo ".$i 00;33"
done

# genomics
for i in {bam,vcf,sam,fastq,fasta,fa,gff,gtf,bed}; do
	echo ".$i 00;32"
done

echo '.ipynb 01;33' # jupyter notebooks

