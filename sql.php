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
            // 获取所有表中所有主键的集合
            $allKeys = $this->getAllKeys();

            // 构建查询语句，以所有主键为基础，查询每个表的对比数据
            $query = "SELECT 
                        k.{$this->prefixColumns($this->keyColumns, 'k')}";
            foreach ($this->compareTables as $table) {
                $query .= ", t_{$table}.{$this->prefixColumns($this->compareColumns, 't_' . $table)}";
            }
            $query .= ", t_{$this->targetTable}.{$this->prefixColumns($this->compareColumns, 't_' . $this->targetTable)}";

            $query .= " FROM (SELECT " . implode(', ', $this->keyColumns) . " FROM (";
            foreach ($allKeys as $key) {
                $query .= "(" . implode(', ', array_map(function ($column) use ($key) {
                    return "'{$key[$column]}'";
                }, $this->keyColumns)) . ") UNION ";
            }
            $query = rtrim($query, " UNION ") . ")) k";

            foreach ($this->compareTables as $table) {
                $query .= " LEFT JOIN {$table} t_{$table} ON " . $this->buildJoinCondition('k', 't_' . $table);
            }
            $query .= " LEFT JOIN {$this->targetTable} t_{$this->targetTable} ON " . $this->buildJoinCondition('k', 't_' . $this->targetTable);

            $result = $this->db->query($query)->getResultArray();

            // 计算比率
            $resultWithRatios = $this->calculateRatios($result);

            return $resultWithRatios;
        } catch (DatabaseException $e) {
            throw new DatabaseException("Database error: " . $e->getMessage());
        }
    }

    protected function getAllKeys()
    {
        $allKeys = [];
        foreach (array_merge($this->compareTables, [$this->targetTable]) as $table) {
            $keys = $this->db->query("
                SELECT " . implode(', ', $this->keyColumns) . "
                FROM {$table}
            ")->getResultArray();
            foreach ($keys as $key) {
                if (!in_array($key, $allKeys)) {
                    $allKeys[] = $key;
                }
            }
        }
        return $allKeys;
    }

    protected function prefixColumns(array $columns, string $prefix)
    {
        return implode(', ', array_map(function ($column) use ($prefix) {
            return "{$prefix}.{$column} AS {$prefix}_{$column}";
        }, $columns));
    }

    protected function buildJoinCondition($table1Alias, $table2Alias)
    {
        $conditions = [];
        foreach ($this->keyColumns as $column) {
            $conditions[] = "{$table1Alias}.{$column} = {$table2Alias}.{$column}";
        }
        return implode(' AND ', $conditions);
    }

    protected function calculateRatios(array $records)
    {
        $ratios = [];
        foreach ($records as $record) {
            $ratioRecord = $record;
            foreach ($this->compareColumns as $column) {
                $targetColumn = "t_{$this->targetTable}_{$column}";
                foreach ($this->compareTables as $table) {
                    $compareColumn = "t_{$table}_{$column}";
                    if (isset($record[$targetColumn]) && isset($record[$compareColumn]) && $record[$compareColumn] != 0) {
                        $ratioRecord["ratio_{$table}_{$column}"] = $record[$targetColumn] / $record[$compareColumn];
                    } else {
                        $ratioRecord["ratio_{$table}_{$column}"] = null;
                    }
                }
            }
            $ratios[] = $ratioRecord;
        }
        return $ratios;
    }
}
