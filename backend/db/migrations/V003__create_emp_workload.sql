-- ============================================================
-- 员工负载表 DDL
-- 版本: V003
-- 说明: 记录每个员工在某营业部下的客户数量和负载等级
--       每次分配/撤回后由 Python 服务立即触发全营业部重算并写入
--       负载分位规则（营业部内从高到低排序）：
--         0.0 ~ 0.2  => 高负载
--         0.2 ~ 0.4  => 偏高
--         0.4 ~ 0.6  => 适中
--         0.6 ~ 0.8  => 偏低
--         0.8 ~ 1.0  => 空闲
-- ============================================================


-- ------------------------------------------------------------
-- 1. 主表
-- ------------------------------------------------------------
CREATE TABLE custgroup.T_EMP_WORKLOAD
(
    ID             NUMBER         NOT NULL,              -- 主键
    BRANCH_NO      VARCHAR2(10)   NOT NULL,              -- 营业部编号
    LOGIN_ID       VARCHAR2(20)   NOT NULL,              -- 员工OA
    EMP_NAME       VARCHAR2(50),                         -- 员工姓名
    CUST_COUNT     NUMBER(6)      DEFAULT 0 NOT NULL,    -- 名下客户总数
    PERCENTILE     NUMBER(5, 4),                         -- 分位值（0~1，越小负载越高）
    LOAD_LEVEL     VARCHAR2(10),                         -- 负载等级: 高负载/偏高/适中/偏低/空闲
    CALC_TIME      TIMESTAMP      DEFAULT LOCALTIMESTAMP, -- 最近一次计算时间
    CONSTRAINT PK_EMP_WORKLOAD PRIMARY KEY (ID),
    CONSTRAINT UQ_EMP_WORKLOAD_EMP UNIQUE (BRANCH_NO, LOGIN_ID)  -- 每个营业部每员工一条
);

COMMENT ON TABLE  custgroup.T_EMP_WORKLOAD                  IS '员工负载表，每次分配撤回后实时重算';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.ID               IS '主键';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.BRANCH_NO        IS '营业部编号';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.LOGIN_ID         IS '员工OA';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.EMP_NAME         IS '员工姓名';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.CUST_COUNT       IS '名下客户总数';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.PERCENTILE       IS '负载分位值，0最高1最低';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.LOAD_LEVEL       IS '负载等级: 高负载/偏高/适中/偏低/空闲';
COMMENT ON COLUMN custgroup.T_EMP_WORKLOAD.CALC_TIME        IS '最近一次计算时间';


-- ------------------------------------------------------------
-- 2. 主键序列
-- ------------------------------------------------------------
CREATE SEQUENCE custgroup.SEQ_EMP_WORKLOAD
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;


-- ------------------------------------------------------------
-- 3. 触发器：INSERT 时自动填充 ID
-- ------------------------------------------------------------
CREATE OR REPLACE TRIGGER custgroup.TRG_EMP_WORKLOAD_ID
    BEFORE INSERT ON custgroup.T_EMP_WORKLOAD
    FOR EACH ROW
BEGIN
    IF :NEW.ID IS NULL THEN
        :NEW.ID := custgroup.SEQ_EMP_WORKLOAD.NEXTVAL;
    END IF;
END;
/


-- ------------------------------------------------------------
-- 4. 索引
-- ------------------------------------------------------------

-- 员工搜索接口：按营业部过滤后按负载排序
CREATE INDEX IDX_EW_BRANCH_LOAD
    ON custgroup.T_EMP_WORKLOAD (BRANCH_NO, CUST_COUNT);

-- 按 LOGIN_ID 快速定位单条记录（负载重算时 MERGE）
CREATE INDEX IDX_EW_LOGIN_ID
    ON custgroup.T_EMP_WORKLOAD (LOGIN_ID);
