多进程使用JDOCK运算分子 docking 的脚本
==================================


copy_files.py
-------------

绝对路径：`/home/program/JDOCK/database/copy_files.py`

将 **\*mol2** 文件拷贝到每个蛋白质文件夹（类似：**1NY3** 的文件夹，共约 2000个 ）下，并根据每个文件夹下的任意一个 **\*_dock.in** 文件，将第一行及第二行的信息替换为 **\*mol2** 文件名称对应的信息，生成新的 **\*_dock.in** 文件。最终的效果应该是每个蛋白质文件夹下新增加了两个文件，一个是拷贝过来的 **\*mol2** 文件，另一个是新生成的 **\*_dock.in** 文件。

对于每个 **\*mol2** 文件，只需要拷贝一次到 2000 个文件夹下即可。

- 切换到 `/home/program/JDOCK/database`下
- 将 **\*.mol2** 文件拷贝到`/home/program/JDOCK/database`下
- 运行 `python copy_files.py`
- 可以通过 **error2016.txt** 查看错误信息。



jdock_multiprocessing.py
------------------------

绝对路径：`/home/program/JDOCK/database/jdock_multiprocessing.py`

对每一个蛋白质文件夹内（共约 2000 个文件夹）新增加的 **\*mol2** 文件和 **\*_dock.in**文件，调用 `/home/program/JDOCK/jdock/jdock` 来进行计算。

- 切换到 `/home/program/JDOCK/database`下
- 修改 **jdock_multiprocessing.py** 脚本，将 `MOL2_FILE_NAME` 替换为新的 **\*mol2** 文件名
- （新脚本会自动清理，不再需要手动进行）运行清理脚本：`python /home/program/JDOCK/database/_jdock_out/delete_incomplete_result_files.py`
- 运行计算脚本：`sudo python run_dock_in.pyjdock_multiprocessing.py`
- 所有输出结果文件均在此目录：`/home/program/JDOCK/database/_jdock_out/$MOL2_FILE_NAME`




extract_energy_score.py
-----------------------

绝对路径：`/home/program/JDOCK/database/_jdock_out/extract_energy_score.py`

对 `/home/program/JDOCK/database/_jdock_out/` 目录下的所有输出文件进行提取，得到 `Energy Score`，`M-Score` 和 `X-Score` 信息。并将信息按照每行`energy_source protein_name m_score x_score` 的形式排列并排序。

- 切换到 `/home/program/JDOCK/database/_jdock_out/` 下
- 运行清理脚本：`python /home/program/JDOCK/database/_jdock_out/delete_incomplete_result_files.py`
- 运行提取脚本：`python extract_energy_score.py`
- 可以查看输出文件：**sorted_energy_scores.txt**




delete_incomplete_result_files.py (expired)
-------------------------------------------

已废弃。新脚本会自动清理，不再需要手动进行。

绝对路径：`/home/program/JDOCK/database/_jdock_out/delete_incomplete_result_files.py`

清理脚本。由于每次计算的时间较长，若意外或人为中断，则仍会在 `/home/program/JDOCK/database/_jdock_out/` 文件夹下生成相应的输出文件，而计算脚本 **run_dock_in.py** 检测到已有相应的输出文件后即会跳过此蛋白的计算，但是此时输出文件由于未计算完成因此并不包含 `Energy Score` 或 `M-Score`，`X-Score` 等信息，不能用于下一步 `extract_energy_score.py` 脚本的信息提取。因此每次在运行计算脚本或者提取脚本之前，需要先运行清理脚本，将由于中断生成的不完全文件删除。

- 运行清理脚本：`python /home/program/JDOCK/database/_jdock_out/delete_incomplete_result_files.py`
