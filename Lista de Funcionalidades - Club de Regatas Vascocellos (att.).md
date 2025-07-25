![][image1]                                                                           ![][image2]

					

**Universidade Estadual de Maringá**

**Centro de Tecnologia**

**Departamento de Informática**

					   **Informática**

                                              **Laboratório de Software**						

					

**Lista de Funcionalidades \- Club de Regatas Vasco Cellos**

                    **Professor: Lilian Passos Scatalon**             
               

| Aluno | RA |
| :---- | :---- |
| **[Bruno Manganoti de Lara](mailto:ra129556@uem.br)** | **129556** |
|  **Felipe Nascimento de Angelis** | **130131** |
| **Gustavo Henrique Sargi Michelim** | **128968** |
| **[Pedro Seiji Tabada](mailto:ra129554@uem.br)** | **129554** |

## **Histórias de usuários**

A seguir estão as **histórias de usuário** correspondentes às funcionalidades descritas no documento. Elas seguem o formato tradicional de *User Stories*:

### **Funcionalidades Essenciais**

**1\. Cadastro Unificado de Usuários**  
 Como administrador,  
 quero cadastrar alunos, voluntários, colaboradores e visitantes em um único sistema,  
 para que eu possa gerenciar todos os tipos de usuários de forma centralizada e eficiente.

**2\. Integração com Leitores Faciais**  
Como operador do sistema,  
quero que os dados biométricos sejam coletados uma única vez e sincronizados com todos os leitores faciais,  
para que os usuários possam ser reconhecidos automaticamente em qualquer ponto de acesso.

**3\. Controle de Acesso por Perfil**  
Como sistema de controle,  
quero validar o acesso com base no tipo de perfil (aluno, visitante, etc.),  
para que cada usuário só acesse os espaços e horários permitidos para seu perfil.

**4\. Relatórios e Logs**  
Como gestor da instituição,  
quero acessar relatórios e históricos de entradas e saídas por usuário, sala e perfil,  
para que eu possa acompanhar e auditar a movimentação dentro da instituição.

**5\. Replicação de Dados entre Leitores**  
Como administrador,  
quero que as informações dos usuários sejam replicadas automaticamente entre os leitores após cada cadastro ou atualização,  
para que não haja necessidade de configurações manuais em cada dispositivo.

**6\. Controle de Presença/Faltas**  
Como coordenador pedagógico,  
quero registrar a presença dos alunos por sala,  
para que eu possa gerar relatórios de frequência de forma precisa.

**Funcionalidades Desejáveis**

**1\. Rota do Usuário**  
Como responsável pela segurança,  
quero visualizar a rota percorrida por um usuário dentro da instituição,  
para que eu possa investigar movimentações suspeitas ou verificar padrões de circulação.

**2\. Melhorias no Cadastro de Visitantes**  
Como recepcionista,  
quero adicionar observações personalizadas e definir um tempo de validade no cadastro de visitantes,  
para que o acesso seja controlado é bloqueado automaticamente após esse período.

**3\. Painel Administrativo Web**  
Como administrador,  
quero acessar um dashboard com estatísticas de presença e acessos,  
para que eu possa monitorar o funcionamento do sistema em tempo real com filtros por período, perfil e local.

**4\. Sistema Multiplataforma (Web \+ Mobile)**  
Como usuário do sistema,  
quero acessar as funcionalidades tanto pelo computador quanto pelo celular,  
para que eu possa acompanhar e operar o sistema de forma flexível e prática.

**5\. Controle de Sessão Ativa**  
Como administrador de segurança,  
quero receber notificações sobre tentativas inválidas de acesso e registrar eventos críticos,  
para que eu possa detectar e agir contra possíveis invasões ou problemas.

### **Funcionalidades de Segurança e Conformidade**

**1\. Conformidade com LGPD**  
Como responsável pelos dados,  
quero obter o consentimento dos usuários no momento do cadastro e permitir o controle ou exclusão de seus dados,  
para que a instituição esteja em conformidade com a LGPD.

**2\. Controle de Acesso Administrativo**  
Como administrador,  
quero definir diferentes perfis de acesso (admin, operador, monitor),  
para que cada usuário tenha acesso apenas às funcionalidades necessárias para sua função.

—------------------------------------------------------------------------------------------------------------------------

## **Funcionalidades Essenciais**

### **1\. Cadastro Unificado de Usuários**

* Cadastro único para alunos, voluntários, colaboradores e visitantes.

* Dados básicos: nome, CPF, foto, horários permitidos de entrada/saída, observações.

* Registro de perfil (aluno, visitante, etc).

### **2\. Integração com Leitores Faciais**

* Coleta única de dados para replicação automática em todos os leitores.

* Compatibilidade com os dispositivos Intelbras.

* Sincronização com múltiplos pontos (salas e portões).

### **3\. Controle de Acesso por Perfil**

* Regras de entrada e saída por tipo de usuário:

  * Aluno: entrada e saída dentro de janelas de tolerância.

  * Visitante: acesso limitado a 24h com observação específica.

* Validação em tempo real.

### 

### 

### 

### **4\. Relatórios e Logs**

* Histórico completo de entradas e saídas por usuário.

* Relatórios por sala, por dia, por perfil.

* Exportação de dados (CSV/PDF).

### **5\. Replicação de Dados entre Leitores**

* Sincronização automática após cadastro/atualização.

### **6\. Controle de Presença/Faltas**

* Registro de presença por sala.

* Geração de relatórios de frequência.

## **Funcionalidades Desejáveis**

### **1\. Rota do Usuário**

* Mapear por onde o usuário passou dentro da instituição.

* Relatório detalhado por horários e salas.

### **2\. Melhorias no Cadastro de Visitantes**

* Campos para observações personalizadas.

* Tempo de validade do cadastro com bloqueio automático.

### **3\. Painel Administrativo Web**

* Dashboard com estatísticas (presença, acessos por hora, etc.).

* Filtros por período, perfil, local.

### 

### 

### **4\. Sistema Multiplataforma (Web \+ Mobile)**

* Acesso via desktop e dispositivos móveis.

* Interface amigável e responsiva.

### **5\. Controle de Sessão Ativa**

* Notificação de tentativas inválidas de acesso.

* Log de eventos críticos.

## **Funcionalidades de Segurança e Conformidade**

### **1\. Conformidade com LGPD**

* Consentimento no cadastro.

* Controle sobre os dados pessoais.

* Permissão de exclusão/desativação de usuários.

### **2\. Controle de Acesso Administrativo**

* Perfis de acesso (admin, operador, monitor).

* Restrições de funcionalidades por perfil.

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>