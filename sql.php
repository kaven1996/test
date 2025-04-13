<?php
namespace App\Libraries;

use CodeIgniter\Database\BaseConnection;
use CodeIgniter\Database\Exceptions\DatabaseException;

class TableComparison
{
    protected $db;
    protected $compareTables; // 对比表数组 (a, b, c)
    protected $targetTable; // 目标表 (d)
    protected $keyColumns; // 主键列数组
    protected $compareColumns; // 对比列数组

    public function __construct(BaseConnection $db, array $compareTables, string $targetTable, array $keyColumns, array $compareColumns)
    {
        $this->db = $db;
        $this->compareTables = $compareTables;
        $this->targetTable = $targetTable;
        $this->keyColumns = $keyColumns;
        $this->compareColumns = $compareColumns;
    }

    public function compare()
    {
        try {
            // 构建查询语句
            $query = "WITH all_keys AS (";
            foreach (array_merge($this->compareTables, [$this->targetTable]) as $table) {
                $query .= "SELECT " . implode(', ', $this->keyColumns) . " FROM {$table} UNION ";
            }
            $query = rtrim($query, ' UNION ') . ") ";

            $query .= "SELECT 
                        k." . implode(', k.', $this->keyColumns);
            foreach ($this->compareTables as $table) {
                $query .= ", " . $table . "." . implode(', ' . $table . '.', $this->compareColumns) . " AS " . $table . "_value1, " . $table . "_value2";
            }
            $query .= ", d." . implode(', d.', $this->compareColumns);

            $query .= " FROM all_keys k";
            foreach (array_merge($this->compareTables, [$this->targetTable]) as $table) {
                $query .= " LEFT JOIN {$table} ON ";
                foreach ($this->keyColumns as $column) {
                    $query .= "k.{$column} = {$table}.{$column} AND ";
                }
                $query = rtrim($query, ' AND ');
            }

            // 执行查询
            $result = $this->db->query($query)->getResultArray();

            // 计算比率
            $resultWithRatios = $this->calculateRatios($result);

            return $resultWithRatios;
        } catch (DatabaseException $e) {
            throw new DatabaseException("Database error: " . $e->getMessage());
        }
    }

    protected function calculateRatios(array $records)
    {
        $ratios = [];
        foreach ($records as $record) {
            $ratioRecord = $record;
            foreach ($this->compareColumns as $column)  ‌‍
