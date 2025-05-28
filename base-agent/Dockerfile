ARG BASE_IMAGE=rayproject/ray:2.42.1-py310-cpu

FROM ${BASE_IMAGE} as builder

USER root

RUN pip install poetry poetry-plugin-export && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* /build/
WORKDIR /build

RUN poetry export -f requirements.txt --without-hashes --output requirements.txt
COPY docker-entrypoint.sh /build/docker-entrypoint.sh
RUN chmod +x /build/docker-entrypoint.sh

FROM ${BASE_IMAGE}

ARG PIP_EXTRA_INDEX_URL
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    python3-dev \
    libgmp-dev \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /build/requirements.txt ./requirements.txt
# Сначала устанавливаем protobuf нужной версии
RUN pip install --no-cache-dir protobuf==5.29.4

# Затем устанавливаем остальные зависимости с флагом --no-deps для protobuf
RUN pip install --no-cache-dir -r ./requirements.txt && \
    rm ./requirements.txt

RUN pip install keyring keyrings.codeartifact

RUN pip install poetry


ENV PIP_INDEX_URL=https://aws:eyJ2ZXIiOjEsImlzdSI6MTc0ODQyOTA2OSwiZW5jIjoiQTEyOEdDTSIsInRhZyI6ImR6SnBDZ1A2RDI2N2ZMYzc5a2o2SFEiLCJleHAiOjE3NDg0NzIyNjksImFsZyI6IkExMjhHQ01LVyIsIml2IjoiREdzeG5sQm5GNWFHM3E5cSJ9.DDQMRrLvFwTm4ypTLYUovw.nREL0VgVz8SY6Uah.588oWyBcQkRiQLE6bzTdGm7Z7jrGp-WWlQCIB0SNHkt0GKny5nP3oKcV_YEB80aAuJB2XaWSHvEpGDEEqVtMc0lBpFgSxX64Dy8nr9kgJy0bwD6fL0JJAcyq3QEqsRnOYKNXIsZfg4jTh9-INy4CMlfl-2wL6AFFnyZ54LhHS_gmOUbCo7guMIcCOghu38Fw-r9wESXXDIis1uDIYqIz881q_DqAQpPRdImiqKO7kEg1jYJIEKx3V2gEE7QJ0dREAVRJhDyhjk3iS36FgfBCJyK9o0UiOZfWp-ZMwx06fV4zDd065k5mbQj2zyejPhxsgd1f6iJbJsfxRMko_CntuR4WDDm6EGo_V_gFI389aHVS5-HMhYQWeAmnozG7Ofk58WM5VUO8J9kunvvxz3U6y-2HXIVwuT5gk-0T0ZKOaXdlKh3Cn4L1EYF_X7Gt7V47IMjjoBMKGEMKRmnp4KJt3C0blsZTHLpdhGkj-Bsp7kmo6f-oEqs3E8wwOgrZ29EFxEpldoHCyAuiKDukwXAhy81xNufzZMcwApha-dTGt-wZrmKwU0ww9NGw_rhRtgkUYdoYyYcP9ts1kG4CKp43XkTMDKua_GZdvM-JGK9P42CfTghTMvzp7NKrEpuNECT9YS4gwTNG2YjwQQL3tWVhlfu57ZOzDQh7cmvm4D5p7uqKKGwFj5mLtYaWxU2hsZzTi-kRYBCL-bCK7htyFV8Nb0TTDLcTt63MgTlqYqe0EWvvh-SiaWd8oj-9BTxwg29Rk8Qs7pJ6IjumuTvETl-Yjlx5zDVXirjqmgrTWFUkYcg67sf1wKmb7Z5evEXhlkCdJns8WQU-qgGGoPzzh59vS4eHeqRl5PcM4iwRtxT0quxP90vHrHWfSQjhVOqG8qnPMwqxrniS2UJ6nkfa9GldmOKjOqwwGTkyitYppldzV15X8qeO9gHtin0mib8WTU1WrdZY8RXocFekTtAp3bgrCNymbEOJ0CPstS2YUnTXWwt7syXCNzMiUJbOSvKHaBQHwDszkxGzZH3Zetkg6f09-bAFQarRNbuZB8iLCC7i5HmNbC-3QdwzyKFM2o9vRi_hjdoq84wb7A9NptAEaiuz507Q3fg8Edceull40GoOb7JkJBQwJuMWEieq_Wbaz2HJbIAOKax0Xejd_T5hEeJJXEe9haC0gn-tVPfzjRCDRQwTR6xkopqU33z8mop-nS1Eo28UHY0E91rO-2hhglK6OKuIhsq1sn1PMz189fIueKoFPvAlLV_86Dzt6kyQCu3I7VAvXk0bsima9vpb6qVHPW9eMC5zawVAfot99dopKLznlDUIrWs.osDcT9mBveb0AAeSx05TSA@pantheon-688567299207.d.codeartifact.eu-west-1.amazonaws.com/pypi/pantheon/simple/
ENV PIP_EXTRA_INDEX_URL=https://aws:eyJ2ZXIiOjEsImlzdSI6MTc0ODQyOTA2OSwiZW5jIjoiQTEyOEdDTSIsInRhZyI6ImR6SnBDZ1A2RDI2N2ZMYzc5a2o2SFEiLCJleHAiOjE3NDg0NzIyNjksImFsZyI6IkExMjhHQ01LVyIsIml2IjoiREdzeG5sQm5GNWFHM3E5cSJ9.DDQMRrLvFwTm4ypTLYUovw.nREL0VgVz8SY6Uah.588oWyBcQkRiQLE6bzTdGm7Z7jrGp-WWlQCIB0SNHkt0GKny5nP3oKcV_YEB80aAuJB2XaWSHvEpGDEEqVtMc0lBpFgSxX64Dy8nr9kgJy0bwD6fL0JJAcyq3QEqsRnOYKNXIsZfg4jTh9-INy4CMlfl-2wL6AFFnyZ54LhHS_gmOUbCo7guMIcCOghu38Fw-r9wESXXDIis1uDIYqIz881q_DqAQpPRdImiqKO7kEg1jYJIEKx3V2gEE7QJ0dREAVRJhDyhjk3iS36FgfBCJyK9o0UiOZfWp-ZMwx06fV4zDd065k5mbQj2zyejPhxsgd1f6iJbJsfxRMko_CntuR4WDDm6EGo_V_gFI389aHVS5-HMhYQWeAmnozG7Ofk58WM5VUO8J9kunvvxz3U6y-2HXIVwuT5gk-0T0ZKOaXdlKh3Cn4L1EYF_X7Gt7V47IMjjoBMKGEMKRmnp4KJt3C0blsZTHLpdhGkj-Bsp7kmo6f-oEqs3E8wwOgrZ29EFxEpldoHCyAuiKDukwXAhy81xNufzZMcwApha-dTGt-wZrmKwU0ww9NGw_rhRtgkUYdoYyYcP9ts1kG4CKp43XkTMDKua_GZdvM-JGK9P42CfTghTMvzp7NKrEpuNECT9YS4gwTNG2YjwQQL3tWVhlfu57ZOzDQh7cmvm4D5p7uqKKGwFj5mLtYaWxU2hsZzTi-kRYBCL-bCK7htyFV8Nb0TTDLcTt63MgTlqYqe0EWvvh-SiaWd8oj-9BTxwg29Rk8Qs7pJ6IjumuTvETl-Yjlx5zDVXirjqmgrTWFUkYcg67sf1wKmb7Z5evEXhlkCdJns8WQU-qgGGoPzzh59vS4eHeqRl5PcM4iwRtxT0quxP90vHrHWfSQjhVOqG8qnPMwqxrniS2UJ6nkfa9GldmOKjOqwwGTkyitYppldzV15X8qeO9gHtin0mib8WTU1WrdZY8RXocFekTtAp3bgrCNymbEOJ0CPstS2YUnTXWwt7syXCNzMiUJbOSvKHaBQHwDszkxGzZH3Zetkg6f09-bAFQarRNbuZB8iLCC7i5HmNbC-3QdwzyKFM2o9vRi_hjdoq84wb7A9NptAEaiuz507Q3fg8Edceull40GoOb7JkJBQwJuMWEieq_Wbaz2HJbIAOKax0Xejd_T5hEeJJXEe9haC0gn-tVPfzjRCDRQwTR6xkopqU33z8mop-nS1Eo28UHY0E91rO-2hhglK6OKuIhsq1sn1PMz189fIueKoFPvAlLV_86Dzt6kyQCu3I7VAvXk0bsima9vpb6qVHPW9eMC5zawVAfot99dopKLznlDUIrWs.osDcT9mBveb0AAeSx05TSA@pantheon-688567299207.d.codeartifact.eu-west-1.amazonaws.com/pypi/agents/simple/https://aws:eyJ2ZXIiOjEsImlzdSI6MTc0ODQyOTA2OSwiZW5jIjoiQTEyOEdDTSIsInRhZyI6ImR6SnBDZ1A2RDI2N2ZMYzc5a2o2SFEiLCJleHAiOjE3NDg0NzIyNjksImFsZyI6IkExMjhHQ01LVyIsIml2IjoiREdzeG5sQm5GNWFHM3E5cSJ9.DDQMRrLvFwTm4ypTLYUovw.nREL0VgVz8SY6Uah.588oWyBcQkRiQLE6bzTdGm7Z7jrGp-WWlQCIB0SNHkt0GKny5nP3oKcV_YEB80aAuJB2XaWSHvEpGDEEqVtMc0lBpFgSxX64Dy8nr9kgJy0bwD6fL0JJAcyq3QEqsRnOYKNXIsZfg4jTh9-INy4CMlfl-2wL6AFFnyZ54LhHS_gmOUbCo7guMIcCOghu38Fw-r9wESXXDIis1uDIYqIz881q_DqAQpPRdImiqKO7kEg1jYJIEKx3V2gEE7QJ0dREAVRJhDyhjk3iS36FgfBCJyK9o0UiOZfWp-ZMwx06fV4zDd065k5mbQj2zyejPhxsgd1f6iJbJsfxRMko_CntuR4WDDm6EGo_V_gFI389aHVS5-HMhYQWeAmnozG7Ofk58WM5VUO8J9kunvvxz3U6y-2HXIVwuT5gk-0T0ZKOaXdlKh3Cn4L1EYF_X7Gt7V47IMjjoBMKGEMKRmnp4KJt3C0blsZTHLpdhGkj-Bsp7kmo6f-oEqs3E8wwOgrZ29EFxEpldoHCyAuiKDukwXAhy81xNufzZMcwApha-dTGt-wZrmKwU0ww9NGw_rhRtgkUYdoYyYcP9ts1kG4CKp43XkTMDKua_GZdvM-JGK9P42CfTghTMvzp7NKrEpuNECT9YS4gwTNG2YjwQQL3tWVhlfu57ZOzDQh7cmvm4D5p7uqKKGwFj5mLtYaWxU2hsZzTi-kRYBCL-bCK7htyFV8Nb0TTDLcTt63MgTlqYqe0EWvvh-SiaWd8oj-9BTxwg29Rk8Qs7pJ6IjumuTvETl-Yjlx5zDVXirjqmgrTWFUkYcg67sf1wKmb7Z5evEXhlkCdJns8WQU-qgGGoPzzh59vS4eHeqRl5PcM4iwRtxT0quxP90vHrHWfSQjhVOqG8qnPMwqxrniS2UJ6nkfa9GldmOKjOqwwGTkyitYppldzV15X8qeO9gHtin0mib8WTU1WrdZY8RXocFekTtAp3bgrCNymbEOJ0CPstS2YUnTXWwt7syXCNzMiUJbOSvKHaBQHwDszkxGzZH3Zetkg6f09-bAFQarRNbuZB8iLCC7i5HmNbC-3QdwzyKFM2o9vRi_hjdoq84wb7A9NptAEaiuz507Q3fg8Edceull40GoOb7JkJBQwJuMWEieq_Wbaz2HJbIAOKax0Xejd_T5hEeJJXEe9haC0gn-tVPfzjRCDRQwTR6xkopqU33z8mop-nS1Eo28UHY0E91rO-2hhglK6OKuIhsq1sn1PMz189fIueKoFPvAlLV_86Dzt6kyQCu3I7VAvXk0bsima9vpb6qVHPW9eMC5zawVAfot99dopKLznlDUIrWs.osDcT9mBveb0AAeSx05TSA@pantheon-688567299207.d.codeartifact.eu-west-1.amazonaws.com/pypi/tools/simple/


WORKDIR /serve_app

COPY py-libp2p /serve_app/py-libp2p

RUN pip install --index-url https://pypi.org/simple/ --no-cache-dir \
    setuptools wheel \
    build \
    trio-asyncio \
    httpx \
    loguru \
    tenacity \
    pydantic-settings \
    base58>=1.0.3 \
    coincurve>=10.0.0 \
    fastecdsa>=1.7.5 \
    grpcio>=1.41.0 \
    lru-dict>=1.1.6 \
    multiaddr>=0.0.9 \
    mypy-protobuf>=3.0.0 \
    noiseprotocol>=0.3.0 \
    protobuf==5.29.4 \
    pycryptodome>=3.9.2 \
    pymultihash>=0.8.2 \
    pynacl>=1.3.0 \
    rpcudp>=3.0.0 \
    trio-typing>=0.0.4 \
    trio>=0.26.0 \
    uvicorn

RUN chmod -R ugo+rwx /serve_app/py-libp2p
WORKDIR /serve_app/py-libp2p
RUN python -m build --wheel --no-isolation --skip-dependency-check .
RUN pip install --no-deps --no-index --find-links=dist/ libp2p

# Force reinstall protobuf 5.29.4 after all dependencies
RUN pip install --force-reinstall protobuf==5.29.4

WORKDIR /serve_app

COPY pyproject.toml /serve_app/pyproject.toml
COPY README.md /serve_app/README.md
COPY src /serve_app/src
COPY entrypoint.py /serve_app/entrypoint.py

COPY --from=builder /build/docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
