-- ---------------------------------------------------------------------------
-- AI 任务执行流水表
-- 记录每一条由 AI 代为执行的员工任务的全生命周期信息
--
-- 来源：员工在「AI 批量处理」页面确认执行后，系统为每条选中任务创建一条记录
-- 状态流转：待执行 → 执行中 → 已完成 / 已失败 / 已撤销
-- ---------------------------------------------------------------------------

CREATE TABLE CUSTGROUP.AIPC_AI_TASKS_LOG (
    -- ── 主键 & 关联 ──────────────────────────────────────────────
    LOG_ID          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- 关联员工任务表（可为 NULL，少数情况是临时任务无对应 TASK_ID）
    TASK_ID         NUMBER,
    CONSTRAINT FK_AITL_TASK FOREIGN KEY (TASK_ID)
        REFERENCES CUSTGROUP.AIPC_STAFF_TASK (TASK_ID) ON DELETE SET NULL,

    -- 执行本次批次的批次号（同一次「一键发起」共享同一 BATCH_ID）
    BATCH_ID        VARCHAR2(36) NOT NULL,   -- UUID，前端生成后传入

    -- ── 任务快照（冗余，方便查询，避免 JOIN）────────────────────
    LOGIN_ID        VARCHAR2(20)  NOT NULL,  -- 所属员工 OA 号
    TASK_TYPE       VARCHAR2(20)  NOT NULL,  -- 建联类/跟进类/周期类/营销活动类/合规类
    TASK_SUB_TYPE   VARCHAR2(50)  NOT NULL,  -- 子类型（如 AI外呼、意向跟进）
    TASK_NAME       VARCHAR2(200) NOT NULL,  -- 任务名称（固定模板名）
    CUST_NO         VARCHAR2(20),            -- 关联客户号（可为空，如批量类任务）
    CUST_NAME_MASKED VARCHAR2(50),           -- 脱敏客户姓名（如 张*明）

    -- ── 执行时间 ─────────────────────────────────────────────────
    SUBMIT_TIME     TIMESTAMP     NOT NULL,                        -- 员工提交批次的时间
    START_TIME      TIMESTAMP,                                     -- AI 实际开始执行时间
    END_TIME        TIMESTAMP,                                     -- AI 执行结束时间（成功/失败均记录）
    DURATION_SEC    NUMBER(10),                                    -- 执行耗时（秒），END_TIME - START_TIME

    -- ── 执行状态 ─────────────────────────────────────────────────
    STATUS          VARCHAR2(10)  DEFAULT '待执行' NOT NULL,
    -- 待执行：已入队，等待 AI 处理
    -- 执行中：AI 正在处理
    -- 已完成：执行成功
    -- 已失败：执行失败（见 FAIL_REASON）
    -- 已撤销：员工主动撤销
    CONSTRAINT CK_AITL_STATUS CHECK (
        STATUS IN ('待执行', '执行中', '已完成', '已失败', '已撤销')
    ),

    -- ── 执行结果 ─────────────────────────────────────────────────
    RESULT_CODE     VARCHAR2(20),   -- 业务结果码，如 CALL_CONNECTED / CALL_BUSY / MSG_SENT
    RESULT_DESC     VARCHAR2(500),  -- 结果描述，如「已拨出，接通，通话时长 2分30秒」
    FAIL_REASON     VARCHAR2(500),  -- 失败原因，STATUS=已失败 时填写，如「电话状态异常」「客户拒接」
    RETRY_COUNT     NUMBER(3) DEFAULT 0 NOT NULL,  -- 已重试次数
    MAX_RETRY       NUMBER(3) DEFAULT 2 NOT NULL,  -- 最大重试次数（可按任务类型配置）

    -- ── AI 执行动作明细（JSON 格式，灵活扩展）────────────────────
    -- 示例：{"action":"call","phone":"138****0001","duration_sec":150,"wechat_added":true}
    ACTION_DETAIL   CLOB,
    CONSTRAINT CK_AITL_JSON CHECK (ACTION_DETAIL IS NULL OR ACTION_DETAIL IS JSON),

    -- ── 合规留痕 ─────────────────────────────────────────────────
    AUDIT_FLAG      CHAR(1) DEFAULT 'N' NOT NULL,  -- Y=已合规审计，N=未审计
    AUDIT_TIME      TIMESTAMP,                      -- 合规审计时间
    AUDIT_REMARK    VARCHAR2(500),                  -- 审计备注

    -- ── 元数据 ───────────────────────────────────────────────────
    CREATE_TIME     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL,
    UPDATE_TIME     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL
);

-- ── 索引 ──────────────────────────────────────────────────────────────────
-- 按员工 + 状态查询（任务大厅「AI执行中」状态条）
CREATE INDEX IDX_AITL_LOGIN_STATUS ON CUSTGROUP.AIPC_AI_TASKS_LOG (LOGIN_ID, STATUS);

-- 按批次号查询（进度弹窗）
CREATE INDEX IDX_AITL_BATCH ON CUSTGROUP.AIPC_AI_TASKS_LOG (BATCH_ID);

-- 按任务号关联
CREATE INDEX IDX_AITL_TASK_ID ON CUSTGROUP.AIPC_AI_TASKS_LOG (TASK_ID);

-- 按提交时间排序（日志流水）
CREATE INDEX IDX_AITL_SUBMIT_TIME ON CUSTGROUP.AIPC_AI_TASKS_LOG (LOGIN_ID, SUBMIT_TIME DESC);

-- ── 注释 ──────────────────────────────────────────────────────────────────
COMMENT ON TABLE  CUSTGROUP.AIPC_AI_TASKS_LOG IS 'AI批量任务执行流水表，记录每条AI代执行任务的全生命周期';
COMMENT ON COLUMN CUSTGROUP.AIPC_AI_TASKS_LOG.BATCH_ID         IS '批次号（UUID），同一次一键发起共享同一值';
COMMENT ON COLUMN CUSTGROUP.AIPC_AI_TASKS_LOG.STATUS           IS '执行状态：待执行/执行中/已完成/已失败/已撤销';
COMMENT ON COLUMN CUSTGROUP.AIPC_AI_TASKS_LOG.RESULT_CODE      IS '业务结果码：CALL_CONNECTED/CALL_BUSY/CALL_REJECTED/MSG_SENT/WECHAT_ADDED 等';
COMMENT ON COLUMN CUSTGROUP.AIPC_AI_TASKS_LOG.ACTION_DETAIL    IS 'AI执行动作明细，JSON格式，字段因任务类型而异';
COMMENT ON COLUMN CUSTGROUP.AIPC_AI_TASKS_LOG.AUDIT_FLAG       IS '合规留痕审计标记：Y=已审计，N=未审计';
