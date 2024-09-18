<br />
<div align="center">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" title="Python" alt="Python" width="200" height="200" />&nbsp;
  <h1 align="center">Aplicaciones Django - Kubernetes Helm & Terraform</h1>
</div>

## Construido con

<p>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="100" height="100" />&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" title="AWS" alt="AWS" width="100" height="100" />&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/kubernetes/kubernetes-original-wordmark.svg" title="K8S" alt="K8S" width="100" height="100" />&nbsp;
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/helm/helm-original.svg" title="Helm" alt="Helm" width="100" height="100" />&nbsp;
</p>

# 📖 Contenido

Este repositorio contiene un proyecto para desplegar dos aplicaciones Django en Kubernetes utilizando Helm y un clúster EKS en AWS. Además, incluye la infraestructura en AWS para persistencia, contenedores y políticas usando Terraform, así como un archivo de configuración para crear un clúster de Kubernetes con `eksctl`.

1. **Despliegue de Aplicaciones Django en Kubernetes con Helm**
   - Dos aplicaciones Django listas para desplegar en Kubernetes.
   - Uso de Helm para empaquetar y gestionar manifiestos de Kubernetes.
   - Configuración de `Ingress Nginx` mediante Helm para gestionar el tráfico externo.

2. **Infraestructura con Terraform**
   - Provisión de infraestructura en AWS:
     - Almacenamiento persistente (S3, RDS, Redis).
     - Repositorios de contenedores (ECR) para almacenar las imágenes Docker.
     - Políticas IAM para gestionar el clúster y recursos asociados.
     - Networking con dos zonas de disponibilidad listas para el clúster EKS.

3. **Creación de un clúster EKS con `eksctl`**
   - Archivo `eksctl` para crear automáticamente un clúster EKS en AWS.

# ⚙️ Requisitos Previos

- [**Kubectl**](https://kubernetes.io/es/docs/reference/kubectl/): Para interactuar con el clúster y aplicar manifiestos.
- [**Lens**](https://docs.k8slens.dev/): Para interactuar visualmente con el clúster.
- [**Kubernetes**](https://kubernetes.io/es/docs/concepts/overview/components/): Se recomienda EKS para este proyecto.
- [**Helm**](https://helm.sh/): Para gestión de charts y despliegues.
- [**eksctl**](https://eksctl.io/): Para crear y gestionar el clúster EKS.
- [**Terraform**](https://www.terraform.io/): Para provisión de infraestructura.
- [**Docker**](https://www.docker.com/): Para construir las imágenes de las aplicaciones.
- [**AWS CLI**](https://aws.amazon.com/es/cli/): Para interactuar con AWS (autenticación y permisos).

# 🛠 Instalación

## 🏗️ 1. Aprovisionar infraestructura

Primero, aprovisionamos la infraestructura necesaria en AWS:

Dentro del proyecto `infra/terraform` tenemos 3 módulos:
- `ecr`: Crea repositorios ECR para las imágenes de las aplicaciones.
- `network-persistence`:  RDS (PostgreSQL), Redis, y networking para EKS.
- `secrets`: Manejo de secrets para las aplicaciones.

```bash
terraform init
terraform plan
terraform apply
```


## ⚓ 2. Creación del clúster de Kubernetes con `eksctl`

Una vez lista la infraestructura, obtenemos la VPC, redes públicas, privadas y conexiones a bases de datos, las cuales almacenaremos en los secrets crearemos el clúster EKS con el archivo `infra/kubernetes/01-eksctl-managed-nodes.yaml`, configurando las variables generadas previamente:



```
    securityGroups:
      attachIDs: ["sg-"]  # Reemplaza con el ID generado por Terraform
    vpc:
      id: "vpc-"  # Reemplaza con el ID generado por Terraform
      subnets:
        private:
          us-west-2a: { id: "subnet-" }  # Reemplaza con el ID de la subnet privada en us-west-2a
          us-west-2b: { id: "subnet-" }  # Reemplaza con el ID de la subnet privada en us-west-2b
        public:
          us-west-2a: { id: "subnet-" }  # Reemplaza con el ID de la subnet pública en us-west-2a
          us-west-2b: { id: "subnet-" }  # Reemplaza con el ID de la subnet pública en us-west-2b

```


Para crear el clúster de Kubernetes, utiliza el siguiente comando de `eksctl`:

```bash
eksctl create cluster -f infra/kubernetes/01-eksctl-managed-nodes.yaml
```

Este proceso tomará aproximadamente 15 minutos. Una vez finalizada la creación del clúster, puedes verificar su estado ejecutando:

```
eksctl get cluster
```

#### Visualización del clúster con Lens  
Para una visualización gráfica del clúster, puedes utilizar la herramienta Lens, que te permitirá interactuar visualmente con los nodos, pods y otros recursos.

En este punto, ya tendrás la infraestructura lista, que incluye dos zonas de disponibilidad,  
una base de datos, y los secrets configurados, listos para ser consumidos por las aplicaciones.

## 🚢 3. Despliegue de aplicaciones con Helm

Una vez creado el clúster, el siguiente paso es desplegar nuestras aplicaciones. Para ello, utilizaremos Helm,  
pero antes debemos instalar algunos paquetes necesarios para la visualización y exposición de nuestro clúster.

### Instalación del servidor de métricas (Metrics Server)
El servidor de métricas te permitirá monitorear el uso de recursos como CPU y memoria en tiempo real dentro del clúster.  

Para instalarlo, ejecuta el siguiente comando:

```
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm upgrade --install metrics-server metrics-server/metrics-server           

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install prometheus prometheus-community/prometheus

```

Valida la instalación con el siguiente comando (el despliegue tardará algunos minutos en estar listo):

```
kubectl get deployment metrics-server -n kube-system
```

### Subida de imágenes Docker a ECR
A continuación, sube las imágenes Docker de tus aplicaciones a los repositorios ECR (Elastic Container Registry) de AWS:

```
docker tag core-application:latest account.dkr.ecr.us-west-2.amazonaws.com/core-application:latest
docker push account.dkr.ecr.us-west-2.amazonaws.com/core-application:latest
```

También puedes hacer uso del CI/CD que contiene el proyecto para empaquetar de manera automatica los cambios de las aplicaciones en cada deploy


### Manejo de secrets en Kubernetes

Para consumir secretos de manera segura en Kubernetes, utilizamos el CSI Driver y AWS Secrets Manager.

#### Instalación de CSI Driver

El CSI Driver permite montar secrets en los pods de Kubernetes de manera segura. Instálalo con los siguientes comandos:

```
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm install csi-secrets-store secrets-store-csi-driver/secrets-store-csi-driver --namespace kube-system --set syncSecret.enabled=true --set enableSecretRotation=true
```

#### Integración con AWS Secrets Manager
Para integrar los secrets con AWS Secrets Manager, instala el siguiente proveedor de CSI:

```
helm repo add aws-secrets-manager https://aws.github.io/secrets-store-csi-driver-provider-aws
helm install -n kube-system secrets-provider-aws aws-secrets-manager/secrets-store-csi-driver-provider-aws
```

#### Instalación de Cert Manager
Para gestionar certificados de dominio, utilizamos Cert Manager. Este gestiona automáticamente los certificados SSL/TLS en Kubernetes.

```
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --set installCRDs=true
```


### Exponer las aplicaciones con Nginx
Para exponer las aplicaciones al exterior, utilizamos Nginx como controlador de ingreso (ingress). Instálalo usando Helm:

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace
```

### Despliegue de las aplicaciones
Finalmente, despliega las aplicaciones Django y los servicios asociados usando los siguientes comandos:

```
helm install release-1 chart
```

Con esto, las aplicaciones estarán desplegadas y accesibles a través de Nginx en tu clúster de Kubernetes.




