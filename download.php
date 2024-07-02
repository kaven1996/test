<?php

namespace App\Controllers;

use CodeIgniter\Controller;
use CodeIgniter\HTTP\RequestInterface;
use App\Models\YourModel;

class DownloadController extends Controller
{
    public function index()
    {
        return view('download_form');
    }

    public function download()
    {
        $request = service('request');
        $link = $request->getPost('link');

        // 下载文件并处理（假设是CSV文件）
        $fileContent = file_get_contents($link);
        $lines = explode("\n", $fileContent);
        
        $model = new YourModel();

        // 清空表数据
        $model->truncate();

        foreach ($lines as $line) {
            $data = str_getcsv($line);
            if (!empty($data)) {
                $model->insert([
                    'column1' => $data[0],
                    'column2' => $data[1],
                    // 根据实际表结构添加列
                ]);
            }
        }

        // 导出CSV文件
        $filename = 'exported_data.csv';
        $data = $model->findAll();
        $csvContent = '';
        
        foreach ($data as $row) {
            $csvContent .= implode(',', $row) . "\n";
        }

        return $this->response->download($filename, $csvContent);
    }
}
