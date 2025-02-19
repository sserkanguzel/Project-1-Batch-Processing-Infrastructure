#Persistent Volume for PostgreSQL (Backed by NFS on TrueNAS)
resource "kubernetes_persistent_volume" "postgres_pv" {
  metadata {
    name = "postgres-pv"
  }
  spec {
    capacity = {
      storage = "100Gi"
    }
    access_modes = ["ReadWriteOnce"]  # Only one pod can write at a time
    persistent_volume_source {
      nfs {
        path   = "/mnt/k8s-storage/postgres"  # Path to NFS share
        server = "192.168.1.100"              # TrueNAS IP (replace with yours)
      }
    }
  }
}

#Persistent Volume Claim for PostgreSQL
resource "kubernetes_persistent_volume_claim" "postgres_pvc" {
  metadata {
    name      = "postgres-pvc"
    namespace = kubernetes_namespace.postgres.metadata[0].name
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "100i"
      }
    }
    volume_name = kubernetes_persistent_volume.postgres_pv.metadata[0].name
  }
}
