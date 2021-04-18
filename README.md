# hog

## histogram of gradient:

**Input**:

<table>
<thead>
<tr>
<th>argument</th>
<th>description</th>
</tr>
</thead>
<tbody>
<tr>
<td>"-n",'--name'</td>
<td>name/path of the image file</td>
</tr>
<tr>
<td>"-d",'--direction'</td>
<td>number of direction</td>
</tr>
<tr>
<td>"-x",'--blockx'</td>
<td>number of blocks on x axis</td>
</tr>
<tr>
<td>"-y",'--blocky'</td>
<td>number of blocks on y axis</td>
</tr>
<tr>
<td>"-b",'--blocksize'</td>
<td>size of the output block</td>
</tr>
</tbody>
</table>

**Output**:

2 plot:
1st with sacle each componant by global maximum
2nd with sacle each componant by local maximum
2 image saved on same directory local.png and global.png
